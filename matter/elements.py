import os
from xml.etree import ElementTree

from gi.repository import Clutter, Gtk, GObject, GdkPixbuf

def getConfig():
    tree = ElementTree.parse("elements.xml")
    return tree.getroot()

class Element(object):
    def getType(self):
        return type(self.element)

class ActorElement(Element):
    def __init__(self, actor):
        self.name = "Actor"
        self.element = actor()

class LayoutElement(Element):
    def __init__(self, layout):
        self.name = "Layout"
        self.element = layout()
        #self.

class ElementGraph(Gtk.TreeStore):
    def __init__(self):
        super(ElementGraph, self).__init__(str, str, GdkPixbuf.Pixbuf)

        icon = GdkPixbuf.Pixbuf.new_from_file("icons/actor-clone.png")

        a = self.append(None, ["foo", "bar", icon])
        b = self.append(None, ['foobar', "barfoo", icon])

        self.append(a, ["eggs", "spam", icon])
        self.append(a, ["spam spam", "eggs", icon])

        self.append(b, ["eggs", "spam", icon])
        self.append(b, ["spam spam", "eggs", icon])