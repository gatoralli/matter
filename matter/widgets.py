from gi.repository import Gtk, GtkClutter, Clutter

class PropertiesEditor(Gtk.Frame):
    def __init__(self):
        super(PropertiesEditor, self).__init__()
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.set_label("Properties")
        # General tab with background color
        self.notebook = Gtk.Notebook()
        self.notebook.append_page(Gtk.Label("General"), Gtk.Label("General"))
        self.add(self.notebook)

class OutlineView(Gtk.Frame):
    def __init__(self):
        super(OutlineView, self).__init__()
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.set_label("Outline")
        
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_shadow_type(Gtk.ShadowType.IN)
        self.treeView = Gtk.TreeView()
        scrolledWindow.add(self.treeView)
        self.add(scrolledWindow)

class ElementPalette(Gtk.ToolPalette):
    def __init__(self):
        super(ElementPalette, self).__init__()
        self.elementItems = []
        self.resetSelected()

    def loadCatalog(self, catalog):
        for group in catalog.groups:
            paletteGroup = Gtk.ToolItemGroup()
            paletteGroup.set_label(group.label)
            self.add(paletteGroup)

            for element in group.elements:
                elementItem = Gtk.ToolItem()

                icon = Gtk.Image()
                icon.set_from_file(element.iconPath)
                button = Gtk.ToggleButton()
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.set_image(icon)

                elementItem.add(button)
                paletteGroup.add(elementItem)
                self.elementItems.append(elementItem)

                button.handler = button.connect("toggled", 
                    self.elementItemToggled, elementItem, element)

    def elementItemToggled(self, button, elementItem, element):
        for item in self.elementItems:
            if elementItem != item:
                itemButton = item.get_child()
                itemButton.handler_block(itemButton.handler)
                itemButton.set_active(False)
                itemButton.handler_unblock(itemButton.handler)

        if button.get_active():
            self.selectedItem = elementItem
            self.selectedElement = element
        else:
            self.resetSelected()

        print "Selected Item: ", self.selectedItem
        print "Selected Element: ", self.selectedElement

    def resetSelected(self):
        self.selectedItem = None
        self.selectedElement = None

class ActorPreview(GtkClutter.Embed):
    def __init__(self):
        super(ActorPreview, self).__init__()

        self.stage = self.get_stage()
        self.stage.set_background_color(Clutter.Color.new(20, 20, 20, 255))

        self.stage.connect("button-press-event", self.mousePress)
        self.stage.connect("button-release-event", self.mouseRelease)
        self.stage.connect("motion-event", self.mouseMove)

        self.box = None
        self.dragState = False
        self.startPos = [0, 0]

    def mousePress(self, actor, event):
        self.dragState = True
        self.box = ActorPreviewBox()
        self.startPos = event.x, event.y
        self.box.set_position(event.x, event.y)

        self.stage.add_actor(self.box)

    def mouseRelease(self, actor, event):
        self.box = None
        self.dragState = False
        self.startPos = [0, 0]

    def mouseMove(self, actor, event):
        if self.dragState is True:
            self.box.set_size(event.x - self.startPos[0], 
                event.y - self.startPos[1])

class ActorPreviewBox(Clutter.Actor):
    def __init__(self):
        super(ActorPreviewBox, self).__init__()

        self.set_background_color(Clutter.Color.new(200, 200, 200, 255))

        subactor = Clutter.Actor()
        subactor.set_background_color(Clutter.Color.new(200, 0, 0, 200))
        subactor.set_size(50, 50)

        self.add_actor(subactor)