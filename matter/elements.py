import os
from xml.etree import ElementTree

from gi.repository import Clutter, Gtk, GObject, GdkPixbuf

def getConfig():
    tree = ElementTree.parse("elements.xml")
    return tree.getroot()


class Element(GObject.GObject):
    
    __gsignals__ = {
        "property-changed": (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_STRING,)),
    }
    
    def __init__(self, elementClass):
        super(Element, self).__init__()
        self.elementClass = elementClass

        self.parent = None
        self.children = []

        self.properties = {}
        self.elementProperties = []
        for prop in self.elementClass.props:
            if prop.flags & GObject.PARAM_READABLE != 0 and prop.flags & GObject.PARAM_WRITABLE != 0:
                self.properties[prop.name] = prop.default_value
                self.elementProperties.append(prop)

        
    def getType(self):
        return self.elementClass.__name__
    
    def createActor(self):
        return self.elementClass()

    def getProperty(self, name):
        return self.properties[name]

    def setProperty(self, name, value, trigger=True):
        self.properties[name] = value
        if trigger:
            self.emit("property-changed", name)

    def loadProperties(self, obj):
        for prop in self.elementClass.props:
            if prop.flags & GObject.PARAM_READABLE != 0 and prop.flags & GObject.PARAM_WRITABLE != 0:
                self.properties[prop.name] = obj.get_property(prop.name)
                #self.setProperty(prop.name, obj.get_property(prop.name))


class StageModel(Gtk.TreeStore):
    
    __gsignals__ = {
        "element-added":
            (GObject.SIGNAL_RUN_FIRST, None, (Element,)),
        "element-removed":
            (GObject.SIGNAL_RUN_FIRST, None, (Element,)),
        "element-selected":
            (GObject.SIGNAL_RUN_FIRST, None, (Element,)),
        "element-property-changed":
            (GObject.SIGNAL_RUN_FIRST, None, (Element, GObject.TYPE_STRING))
    }
    
    def __init__(self):
        super(StageModel, self).__init__(str, str, GdkPixbuf.Pixbuf)
        self.nodes = {}
        self.selectedElement = None
        
        self.icon = GdkPixbuf.Pixbuf.new_from_file("icons/actor-clone.png")
        
        self.stage = Element(Clutter.Stage)
        self.addElement(self.stage, None)

    def deleteElement(self, path):
        self.remove(self.get_iter(path))
        
    def focusOn(self, element):
        self.filter_new(element)
        
    def addElement(self, element, parent):
        # Add element to the model
        parentNode = None
        if parent:
            parentNode = self.nodes[parent]
        print "parent ", parentNode
        node = self.append(parentNode, [element.getProperty("name"), 
            element.getType(), self.icon])
        self.nodes[element] = node

        element.connect("property-changed", self.onElementPropertyChanged)

        if element.parent:
            element.parent.children.append(element)
        element.parent = parent

        self.emit("element-added", element)

        for child in element.children:
            self.addElement(child, element)
    
    def removeElement(self, element):
        # TODO: element.propertyChangedHandler.disconnect()

        if element.parent:
            element.parent.children.remove(element)
        element.parent = None

        self.emit("element-removed", element)

        for child in element.children:
            self.removeElement(child)
    
    def selectElement(self, element):
        if self.selectedElement != element:
            self.selectedElement = element
            self.emit("element-selected", element)
    
    def onElementPropertyChanged(self, element, name):
        if name == "name":
            node = self.nodes[element]
            self.set_value(node, 0, element.getProperty("name"))
        self.emit("element-property-changed", element, name)