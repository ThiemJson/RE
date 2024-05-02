import os
import yaml
import logging
import sys

from treqs.list_elements import list_elements

class check_elements:

    def __init__(self):
        self.__logger = logging.getLogger('treqs-on-git.treqs-ng')
        self.__list_elements = list_elements()
        self.__ttim_types=dict()
        self.__ttim_required=dict()

        self.__element_dict=dict()
        self.__no_type_list = []
        self.__duplicate_id_dict = dict()
        self.__invalid_id_list = []

        self.__logger.log(10,'check_elements created')
    
    def __check_treqs_element_list(self, element_list):
        success = 0

        self.__logger.log(20, "| Error location | Error | File:Line |")
        self.__logger.log(20, "| :--- | :--- | :--- |")

        #Actually check each individual element
        for element in element_list:
            if self.__check_treqs_element(element) != 0:
                success = 1            
        
        #Post-hoc check: Now that the __element_id_set is complete, we can check whether targets exist and their types are fitting
        for element in element_list:
            #Only process valid elements
            if element.treqs_type in self.__ttim_types:
                for link in element.outlinks:
                    #Only process link types that are recognized per TTIM
                    if link.tlt in self.__ttim_types[element.treqs_type]:
                        if not link.target in self.__element_dict:
                            success = 1
                            self.__logger.log(30,"| Element %s | Element references non-existent element with id %s | %s:%s |",  element.uid, link.target, element.file_name, element.placement)
                        else:
                            #If the link has a target type constraint, check whether it is met
                            if self.__ttim_types[element.treqs_type][link.tlt] is not None:
                                if not is_type_contained(self.__element_dict[link.target].treqs_type, self.__ttim_types[element.treqs_type][link.tlt]):
                                    success = 1
                                    if type(self.__ttim_types[element.treqs_type][link.tlt]) != list:
                                        self.__logger.log(30,"| Element %s | '%s' link to element %s needs to point to a %s, but points to a %s instead. | %s:%s |", element.uid, link.tlt, link.target, self.__ttim_types[element.treqs_type][link.tlt], self.__element_dict[link.target].treqs_type, element.file_name, element.placement)
                                    elif len(self.__ttim_types[element.treqs_type][link.tlt]) == 1:
                                        self.__logger.log(30,"| Element %s | '%s' link to element %s needs to point to a %s, but points to a %s instead. | %s:%s |", element.uid, link.tlt, link.target, self.__ttim_types[element.treqs_type][link.tlt][0], self.__element_dict[link.target].treqs_type, element.file_name, element.placement)
                                    else:
                                        self.__logger.log(30,"| Element %s | '%s' link to element %s needs to point to one of these %s, but points to a %s instead. | %s:%s |", element.uid, link.tlt, link.target, self.__ttim_types[element.treqs_type][link.tlt], self.__element_dict[link.target].treqs_type, element.file_name, element.placement)

        #Reporting: List all check errors
        if len(self.__duplicate_id_dict) != 0:
            for element, file_name in self.__duplicate_id_dict.items():
                self.__logger.log(30,"| Element %s | Element id is duplicated. | %s:%s |", element.uid, file_name, element.placement)
        
        if len(self.__invalid_id_list) != 0:
            for element in self.__invalid_id_list:
                self.__logger.log(30,"| Element type %s | Element does not have an id. | %s:%s |", element.treqs_type, element.file_name, element.placement)
        
        if len(self.__no_type_list) != 0:
            for element in self.__no_type_list:
                self.__logger.log(30,"| Element %s | Element has an empty or missing type. | %s:%s |", element.uid, element.file_name, element.placement)
        
        return success

    def check_elements(self, file_name, recursive, ttim_path):
        self.__logger.log(10,'Processing TTIM at %s', ttim_path)
        success = self.load_ttim(ttim_path)

        if success == 0:
            #If TTIM processed successfully, traverse the file tree with the XML strategy and the XPath selector to get all treqs-elements somewhere in the tree.
            element_list = self.__list_elements.get_element_list(file_name, None, recursive)
            success = self.__check_treqs_element_list(element_list)

        if success == 0:
            self.__logger.log(10,"treqs check exited successfully.")
        else: 
            self.__logger.log(30,"treqs check exited with failed checks.")
            
        sys.exit(success)

    def __check_treqs_element(self, element):
        success = 0

        #Check for empty types
        if element.treqs_type == "" or element.treqs_type == None:
            success = 1
            self.__no_type_list.append(element)
        
        #Check for empty ids
        if element.uid == "" or element.uid == None:
            success = 1
            self.__invalid_id_list.append(element)
        
        #Check for duplicate ids
        if element.uid in self.__element_dict:
            success = 1
            self.__duplicate_id_dict[element] = element.file_name
        else:
            self.__element_dict[element.uid] = element

        #Only process types that are recognized per TTIM
        if not element.treqs_type in self.__ttim_types:
            self.__logger.log(30,'| Element %s | Element has an unrecognized type: %s | %s:%s |', element.uid, element.treqs_type, element.file_name, element.placement)
            return 1
        else:
            #make a copy of our ttim required links that we can then 'tick off'
            missing_traces = self.__ttim_required[element.treqs_type].copy()
            for link in element.outlinks:
                #Only process link types that are recognized per TTIM
                if not link.tlt in self.__ttim_types[element.treqs_type]:
                    self.__logger.log(30,'| Element %s | Unrecognised link type %s within element of type %s. | %s:%s |', element.uid, link.tlt, element.treqs_type, element.file_name, element.placement) 
                    success = 1
                else:
                    #"Cross off" required links
                    #Check whether outgoing required traces exist
                    if link.tlt in missing_traces:
                        missing_traces.remove(link.tlt)

            if len(missing_traces) > 0:
                self.__logger.log(30,'| Element %s |  Required links missing: %s | %s:%s |', element.uid, missing_traces, element.file_name, element.placement)
                success = 1
              
        return success

    def load_ttim(self, ttim_path):
        if os.path.isfile(ttim_path):
            # Open the ttim
            with open(ttim_path) as ttim_file:
                ttim_json = yaml.safe_load(ttim_file)

                #Process TTIM    
                for current_type in ttim_json["types"]:
                    #Extract all types
                    self.__ttim_types[current_type['name']] = dict()
                    self.__ttim_required[current_type['name']] = []
                    
                    #TODO: Add support for incoming required traces (A "type" needs to have a "relateTo" from at least one other "type")

                    #For each type, save all allowed trace types (outgoing traces)
                    for current_link in current_type["links"]:
                        if "target" in current_link.keys():
                            if type(current_link["target"]) != list:
                                current_link_target = current_link["target"]
                            else:
                                if len(current_link["target"]) == 1:
                                    current_link_target = current_link["target"][0]
                                else:
                                    current_link_target = current_link["target"]
                            self.__ttim_types[current_type['name']][current_link["type"]] = current_link_target
                        else :
                            self.__ttim_types[current_type['name']][current_link["type"]] = None
                        if "required" in current_link.keys():
                            self.__ttim_required[current_type['name']].append(current_link["type"])
                            

                self.__logger.log(10,'Types and their links according to TTIM: %s', self.__ttim_types)
                return 0

        #TODO: we want to devise a strategy for graceful error handling at some point
        else:
            self.__logger.log(40,'TTIM could not be loaded at %s', ttim_path)
            return 1

    # def extract_label(self, text):
    #     # It is our convention to use the first none-empty line as label
    #     ret = "None"
    #     for line in text.splitlines():
    #         if line != "" and ret == "None":
    #             ret = line
    #     return ret


# This functions checks whether a treqs-type exists in a list of treqs-type
# This has been added to allow for backwards compatability where link targets could be a single treqs-type
# In order not to break links where the target is a single type AND allow for multi-type targets
# The functions checks for the Python type of the treqs_type_list variable
# and performs the logical comparison corresponding to the Python type.
def is_type_contained(treqs_type, treqs_type_list):
    return treqs_type in treqs_type_list if type(treqs_type_list) == list else treqs_type == treqs_type_list
