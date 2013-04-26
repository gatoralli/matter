from xml.etree import ElementTree
from gi.repository import Clutter
import elements

class ElementCatalog(object):
    def __init__(self, path):
        self.element = ElementTree.parse(path).getroot()
        self.groups = []
        self.loadElements()

    def loadElements(self):
        for itemGroup in self.element.findall("*element-group"):
            elementGroup = ElementGroup(itemGroup.get("label"), 
                itemGroup.get("expanded") == "True", 
                itemGroup.get("class"))
            self.groups.append(elementGroup)

            for item in itemGroup.findall("element"):
                icon = self.element.find("*icon[@id='%s']" % 
                    item.get("icon-id"))
                element = Element(item.get("label"), item.get("class"), 
                    icon.get("path"), elementGroup)
                elementGroup.elements.append(element)


class ElementGroup(object):
    def __init__(self, label, expanded, itemClass):
        self.label = label
        self.expanded = expanded
        self.itemClass = getattr(elements, itemClass)
        self.elements = []

class Element(object):
    def __init__(self, label, itemClass, iconPath, parent):
        self.label = label
        self.itemClass = getattr(Clutter, itemClass)
        self.iconPath = iconPath
        self.parent = parent