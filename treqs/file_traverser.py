import os
from lxml import etree as ET
import logging
import glob

class file_traverser:
    def __init__(self):
        self.__logger = logging.getLogger('treqs-on-git.treqs-ng')
        self.__logger.log(10,'file_traverser created')
        # TODO We hardcode the filename to .treqs-ignore. This can be reconsidered.
        self.ignore_list = self.import_treqs_ignore('.treqs-ignore')
        self.compiled_recursive_ignore_list = self.compile_ignore_list(recursive=True)
        self.compiled_non_recursive_ignore_list = self.compile_ignore_list(recursive=False)


    def traverse_file_hierarchy(self, path, recursive, handler, traversal_strategy = "", element_selector = ""):
        '''
        Iterates over all files in a given directory (potentially recursive).
        For each file, the provided handler function is called
        '''
        success = 0
        # A specific traversal strategy function can be provided.
        # If none is provided, call the generic one (calling the handler for each file with a file name attribute)
        if traversal_strategy == "":
            self.__logger.log(10,"Choosing generic traversal strategy")
            traversal_strategy = self.traverse_generic_file
            
        if not path:
            path = '.' # no file or directory specified
        #If a wildcard was provided, this is automatically resolved into a tuple of filenames. Process these here.
        if type(path) == tuple: # regex pattern was specified and file_name is of type tuple with filenames that match the pattern inside.
            for filename in path:
                if os.path.exists(filename) and os.path.isfile(filename):
                    if traversal_strategy(filename, handler, element_selector) != 0:
                        success = 1
                else:
                    if self.__traverse_directory(filename, True, handler, traversal_strategy, element_selector) != 0:
                        success = 1
        elif not os.path.exists(path):
            self.__logger.log(30,"\n\n### File or directory %s does not exist. Skipping.", path)
            success = 1
        elif os.path.isfile(path):
            success = traversal_strategy(path, handler, element_selector)
        else:
            success = self.__traverse_directory(path, recursive, handler, traversal_strategy, element_selector)
            
        return success

    def __traverse_directory (self, path, recursive, handler, traversal_strategy = "", element_selector = ""):
        '''
        Takes care of the traversal of a directory. Used as a helper in the overall traversal.
        '''
        success = 0

        #sorting the return list of files to improve testability and generally lead to less flaky behaviour in case of errors
        if recursive:
            for root, directories, filenames in os.walk(path, topdown=True):
                if root.startswith("./"):
                    root = root[2:]
                if root.endswith("/"):
                    root = root[:-1]

                #removes ignored directories in place, so that traversing them is avoided
                directories[:] = [d for d in directories if not self.filename_is_ignored(os.path.join(root, d) ,recursive)]

                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if self.filename_is_ignored(file_path ,recursive) == True:
                        self.__logger.log(10,"   ### Ignoring file %s (.treqs-ignore)", file_path)
                        continue
                    if traversal_strategy(file_path, handler, element_selector) != 0:
                        success = 1                  
        else:
            if path.startswith("./"):
                path = path[2:]
            if path.endswith("/"):
                path = path[:-1]

            listOfFiles = sorted(os.listdir(path))    
            for filename in listOfFiles:
                file_path = os.path.join(path, filename)
                if os.path.isdir(file_path):
                    self.__logger.log(10,"\n\n### Non-recursive file_traverser, skipping directory %s", file_path )
                    continue
                if self.filename_is_ignored(file_path ,recursive) == True:
                    self.__logger.log(10,"   ### Ignoring file %s (.treqs-ignore)", file_path)
                    continue
                if traversal_strategy(file_path, handler, element_selector) != 0:
                    success = 1
        return success

    def import_treqs_ignore(self, treqs_ignore_file):
        '''Imports filename patterns from the .treqs-ignore file'''
        ignore_list = []
        try:
            with open(treqs_ignore_file, 'r') as ti:
                ignore_list = ti.read().splitlines()
                return ignore_list
        except FileNotFoundError:
            return ignore_list
    def compile_ignore_list(self,recursive):
        result = []
        for pattern in self.ignore_list:
            for f in glob.glob(pattern, recursive=recursive):
                result.append(f)
        return result

    def filename_is_ignored(self, file_name, recursive):
        if recursive:
            return file_name in self.compiled_recursive_ignore_list
        else:
            return file_name in self.compiled_non_recursive_ignore_list

    def traverse_XML_file(self, file_name, handler, element_selector = ""):
        '''
        Traversal strategy for XML files.
        Iterates over all elements selected using the element_selector XPath statement.
        Calls the handler funct with file name and the current element.
        '''
        success = 0
        self.__logger.log(10,"\n\nCalling XML traversal with filename %s", file_name)
        try:
            self.__logger.log(10,'   ### Processing elements in File %s', file_name)

            #We are reading in the file as a string and add "fake" root tags around, then feed into the XML parser
            #This allows us to find treqs tags even in non-XML files using an XML parser.
            with open(file_name) as xml_file:
                xml_file_string = xml_file.readlines()

            #Quickfix: Remove plantuml
            #TODO We might in the future want to support different exclusion criteria depending on file type
            lines = ""
            cut = False
            for line in xml_file_string:
                if cut:
                    if line.find("@end") != -1:
                        self.__logger.log(10,'   End of plantuml tag.')
                        cut = False
                else:
                    if line.find("@start") != -1:
                        self.__logger.log(10,'   Found plantuml tag. Ignoring...')
                        cut = True
                    else:
                        lines += line

            xml_file_string = lines
            #Quickfix: end

            #If there is an element_selector, we use this string as an XPath selector to select elements
            #NOTE ElementTree does not support all of XPath. Maybe we want to consider replacing this at some point if we see the need for sophisticated queries.
            if element_selector != "":
                xml_file_string = "<treqs>" + xml_file_string + "</treqs>"
                root = ET.fromstring(xml_file_string)

                for element in root.findall(element_selector):
                    if handler(file_name, element) != 0:
                        success = 1

            #If there is no element_selector, we assume that the relevant elements are directly under the root.
            #We also assume that the document has a root tag.
            else:
                root = ET.fromstring(xml_file_string)
                for element in root:
                    if handler(file_name, element) != 0:
                        success = 1

        #Currently just ignore parse errors - we consider this a success for now
        except ET.ParseError as err:
            self.__logger.log(10,'   ### Skipping elements in File %s due to parser error (%s)', file_name, str(err.args))
            return 0

        except UnicodeDecodeError:
            self.__logger.log(10,'   ### Skipping elements in File %s due to UnicodeDecodeError', file_name)
            return 0            

        return success

    # Generic traversal strategy. Just calls the handler with the file name attribute.
    # The handler function decides what to do with the file
    # NOTE Currently the element_selector is unused, but we might consider just searching for it in terms of a full-text search. In that case, unclear what we'd return, though.
    def traverse_generic_file(self, file_name, handler, element_selector = ""):
        self.__logger.log(10,'   ### Processing elements in File %s', file_name)
        return handler(file_name)
