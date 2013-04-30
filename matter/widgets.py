from gi.repository import Gtk, GtkClutter, Clutter, GObject

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
    def __init__(self, model):
        super(OutlineView, self).__init__()
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.set_label("Outline")
        
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_shadow_type(Gtk.ShadowType.IN)

        self.treeView = Gtk.TreeView(model)


        box = Gtk.CellAreaBox()
        column = Gtk.TreeViewColumn.new_with_area(box)

        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        box.set_spacing(2)

        # Icon
        iconRenderer = Gtk.CellRendererPixbuf()
        iconRenderer.props.xpad = 2
        box.pack_start(iconRenderer, False, True, False)
        column.add_attribute(iconRenderer, "pixbuf", 2)

        # Element Name
        nameRenderer = Gtk.CellRendererText()
        box.pack_start(nameRenderer, False, True, False)
        column.add_attribute(nameRenderer, "text", 0)
        
        # Padding
        paddingRenderer = Gtk.CellRendererText()
        paddingRenderer.props.width = 8
        box.pack_start(paddingRenderer, False, True, False)

        # Class Name / Details
        classNameRenderer = Gtk.CellRendererText()
        box.pack_start(classNameRenderer, False, True, False)
        column.add_attribute(classNameRenderer, "text", 1)
        
        self.treeView.append_column(column)
        self.treeView.set_headers_visible(False)
        # self.treeView.set_reorderable(True)
        self.setModel(model)

        scrolledWindow.add(self.treeView)
        self.add(scrolledWindow)

    def setModel(self, model):
        self.treeView.set_model(model)

class ElementPalette(Gtk.ToolPalette):
    def __init__(self):
        super(ElementPalette, self).__init__()

        GObject.signal_new("element-changed", ElementPalette, 
            GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, 
            GObject.TYPE_NONE, (GObject.TYPE_STRING,))
        
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
                button.set_tooltip_text(element.label)

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

        self.emit("element-changed", self.selectedElement)

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

        self.elementClass = None

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
        if self.elementClass:
            # Brush Mode
            if self.dragState is True:
                self.box.set_size(event.x - self.startPos[0], 
                    event.y - self.startPos[1])
            element = self.stage.get_actor_at_pos(Clutter.PickMode.ALL, event.x, event.y)
            print element.get_layout_manager()
        else:
            # Select Mode
            pass
    
    def setElementClass(self, elementClass):
        self.elementClass = elementClass
        print elementClass
        #print element

class ActorPreviewBox(Clutter.Actor):
    def __init__(self):
        super(ActorPreviewBox, self).__init__()
        self.set_background_color(Clutter.Color.new(200, 200, 200, 255))