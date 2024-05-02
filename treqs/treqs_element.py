import logging
from typing import Dict

class treqs_element:

    def __init__(self,element, file_name):
        self.uid = element.get("id")
        self.text = element.text
        self.label = self.extract_label(element.text)
        self.treqs_type = element.get("type")
        self.file_name = file_name
        self.outlinks = []
        self.inlinks = []
        self.placement = element.sourceline
        for treqslink in element.iter('treqs-link'):
            tl = treqs_link(self.uid, treqslink, file_name)
            self.outlinks.append(tl)

    def extract_label(self, text):
        # It is our convention to use the first none-empty line as label
        ret = "None"
        for line in text.splitlines():
            if line != "" and ret == "None":
                ret = line

        return ret
    
    def __str__(self) -> str:
        ret_str = (f"| {self.uid} | {self.treqs_type} | {self.label} | {self.file_name}:{self.placement} |")
        return ret_str

class treqs_link:
    def __init__(self, source, treqslinkelement, file_name):
        self.source = source # expect treqs_element's uid 
        self.target = treqslinkelement.get('target') # extract from text
        self.tlt = treqslinkelement.get('type') # extract tracelink type from text
        self.placement = treqslinkelement.sourceline
        self.file_name = file_name

class treqs_element_factory():

    _treqs_elements: Dict[str, treqs_element] =  {}

    def __init__(self) -> None:
        self.__logger = logging.getLogger('treqs-on-git.treqs-ng')
        self.__logger.log(10,'treqs_element_factory created')


    def get_treqs_element(self, element, file_name) -> treqs_element:
        # Let's cache treqs elements for later use.
        key = str(element.get("id"))+str(file_name)+str(element.sourceline)

        if not self._treqs_elements.get(key):
            self._treqs_elements[key] = treqs_element(element, file_name)

        return self._treqs_elements[key]

    def process_inlinks(self): 
        for te in self._treqs_elements.values():
            te.inlinks.clear()

        for te in self._treqs_elements.values():
            for tl in te.outlinks:
                target_te = self.get_element_with_uid(tl.target)
                if target_te is not None:
                    target_te.inlinks.append(tl)

    def get_element_with_uid(self, uid):
        if uid is None:
            return None
        for key in self._treqs_elements.keys():
            if key.startswith(uid):
                return self._treqs_elements[key]
        return None
