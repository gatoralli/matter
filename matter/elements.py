import os
from xml.etree import ElementTree

from gi.repository import Clutter

def getConfig():
    tree = ElementTree.parse("elements.xml")
    return tree.getroot()

class Element(object):
    def __init__(self):
        self.name = None

class ActorElement(Element):
    def __init__(self, actor):
        self.name = "Actor"
        self.element = actor

class LayoutElement(Element):
    def __init__(self, layout):
        self.name = "Layout"
        self.element = layout