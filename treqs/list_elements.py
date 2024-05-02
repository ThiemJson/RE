import os.path
import xml.etree.cElementTree as ET
import logging
import sys

from treqs.treqs_element import *
from treqs.file_traverser import file_traverser
from enum import Enum


class list_elements:
    class Direction(Enum):
        INWARDS = "inlinks"
        OUTWARDS = "outlinks"

    def __init__(self):
        self.__logger = logging.getLogger('treqs-on-git.treqs-ng')
        self.traverser = file_traverser()
        self.element_list = []
        self.treqs_element_factory = treqs_element_factory()
        self.__logger.log(10, 'list_elements created')
        self.__interesting_elements = set()  # This is a set, to keep track of relevant Treqs objects

    def list_elements(self, file_name, treqs_type, recursive, uid, outlinks, inlinks):
        self.get_element_list(file_name, treqs_type, recursive, uid, outlinks, inlinks)
        self.log_element_list()
        sys.exit(0)

    def list_elements_as_plantuml(self, filename, type, outlinks, inlinks, recursive=True, uid=None):
        self.get_element_list(filename, type, recursive, uid, outlinks=outlinks, inlinks=inlinks)
        self.__logger.log(20, "@startuml")
        if len(self.element_list) != 0:
            for element in self.element_list:
                self.__interesting_elements.add(element.uid)
                self.log_element_as_plantuml_object(element)
            if inlinks:
                for element in self.element_list:
                    self.log_links_as_plantuml(element, self.Direction.INWARDS)
            if outlinks:
                for element in self.element_list:
                    self.log_links_as_plantuml(element, self.Direction.OUTWARDS)

        self.__logger.log(20, "@enduml")
        sys.exit(0)

    def log_element_as_plantuml_object(self, element, fallback_uid="No UID"):
        if element is None:  # This element is out of scope
            self.__logger.log(20, 'map "**%s**" as %s {', "OUT OF SCOPE ELEMENT",
                              self.__safe_plantuml_uid(fallback_uid))
            self.__logger.log(20, 'uid => ""%s""', fallback_uid)
            self.__logger.log(20, '}')

            return

        self.__logger.log(20, 'map "**%s**" as %s {', element.label, self.__safe_plantuml_uid(element.uid))
        self.__logger.log(20, 'uid => ""%s""', element.uid)
        self.__logger.log(20, 'type => //%s//', element.treqs_type)
        self.__logger.log(20, 'location => %s:%s', element.file_name.replace("/", "/\\n"), element.placement)
        self.__logger.log(20, '}')

    def log_links_as_plantuml(self, element, direction):
        links = element.inlinks if direction == self.Direction.INWARDS else element.outlinks
        arrows = "-->"

        for tl in links:
            link_target = tl.source if direction == self.Direction.INWARDS else tl.target
            if link_target not in self.__interesting_elements:
                self.__interesting_elements.add(link_target)
                target_treqs_element = self.treqs_element_factory.get_element_with_uid(link_target)
                self.log_element_as_plantuml_object(target_treqs_element, fallback_uid=link_target)

            if direction == self.Direction.INWARDS:
                self.__logger.log(20, '%s %s %s : %s', self.__safe_plantuml_uid(link_target), arrows,
                                  self.__safe_plantuml_uid(element.uid), tl.tlt)
            elif direction == self.Direction.OUTWARDS:
                self.__logger.log(20, '%s %s %s : %s', self.__safe_plantuml_uid(element.uid), arrows,
                                  self.__safe_plantuml_uid(link_target), tl.tlt)

    @staticmethod
    def __safe_plantuml_uid(uid):
        return uid.replace("-", "_")

    def log_element_list(self):
        self.__logger.log(20, "| UID | Type | Label | File:Line |")
        self.__logger.log(20, "| :--- | :--- | :--- | :--- |")
        if len(self.element_list) != 0:
            for element in self.element_list:
                self.__logger.log(20, "%s", element)
                if (self.list_outlinks):
                    self.log_outlinks(element)
                if (self.list_inlinks):
                    self.log_inlinks(element)

        return

    def get_element_list(self, file_name, treqs_type=None, recursive=True, uid=None, outlinks=False, inlinks=False):
        self.treqs_type = treqs_type
        self.uid = uid
        self.list_outlinks = outlinks
        self.list_inlinks = inlinks
        self.traverser.traverse_file_hierarchy(file_name, recursive, self.extract_treqs_element,
                                               self.traverser.traverse_XML_file, ".//treqs-element")

        # After we have the entire element inventory, we process
        if (self.list_inlinks):
            self.process_inlinks()

        return self.element_list

    def extract_treqs_element(self, file_name, element):
        te = self.treqs_element_factory.get_treqs_element(element, file_name)
        # Filter by type - return if the current element is not the one we filter for.
        if self.treqs_type is not None and self.treqs_type != te.treqs_type:
            return 
        # Filter by ID - return if the current element does not have the right ID.
        if self.uid is not None and self.uid != te.uid:
            return 

        # If not filtered, we append the Treqs element to our list
        self.element_list.append(te)

    def log_outlinks(self, element):
        for tl in element.outlinks:
            target_treqs_type = self.treqs_element_factory.get_element_with_uid(tl.target)
            if target_treqs_type == None:
                label = 'Target treqs element not found. Has the containing file been included in the scope?'
                file_line = "--"
            else:
                label = target_treqs_type.label
                file_line = "{file}:{line}".format(file=target_treqs_type.file_name,line=target_treqs_type.placement)
            self.__logger.log(20,'| --outlink--> (%s) | %s | Target: %s | %s |', tl.target, tl.tlt, label, file_line)

    def log_inlinks(self, element):
        for tl in element.inlinks:
            source_te = self.treqs_element_factory.get_element_with_uid(tl.source)
            label = source_te.label
            file_line = "{file}:{line}".format(file=source_te.file_name, line=source_te.placement)
            self.__logger.log(20,'| --inlink--> (%s) | %s | Source: %s | %s |', tl.source, tl.tlt, label, file_line )

    def process_inlinks(self):
        for te in self.element_list:
            self.treqs_element_factory.process_inlinks()
