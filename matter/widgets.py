from gi.repository import Gtk, Gdk, GtkClutter, Clutter, GObject, Cogl
from pprint import pprint
import random

from elements import Element


class PropertiesEditor(Gtk.Frame):
    def __init__(self, model):
        super(PropertiesEditor, self).__init__()
        self.currentElement = None
        self.editors = {}
        
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.set_label("Properties")
        # General tab with background color
        self.notebook = Gtk.Notebook()

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid.set_margin_top(5)
        self.grid.set_margin_bottom(5)
        self.grid.set_margin_left(5)
        self.grid.set_margin_right(5)

        self.scrolledWindow = Gtk.ScrolledWindow()
        #self.scrolledWindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        self.viewport = Gtk.Viewport()
        self.viewport.add(self.grid)
        self.scrolledWindow.add(self.viewport)

        self.scrolledWindow.show_all()#self.grid.show_all()

        self.notebook.append_page(self.scrolledWindow, Gtk.Label("General"))
        self.add(self.notebook)
        self.setModel(model)
        
    def setModel(self, model):
        self.clear()
        self.model = model
        self.model.connect("element-selected", self.setElement)
        self.model.connect("element-property-changed", 
                           self.onElementPropertyChanged)
        
    def addEditor(self, editor):
        self.editors[editor.param.name] = editor

        label = Gtk.Label("%s:" % editor.param.nick)
        label.set_alignment(0.0, 0.5)
        self.grid.add(label)
        self.grid.attach_next_to(editor.widget, label, Gtk.PositionType.RIGHT, 4, 1)
        editor.widget.set_hexpand(True)
        label.show()
        editor.widget.show()
        
    def setElement(self, obj, element):
        if self.currentElement != element:
            self.clear()
            self.currentElement = element
            for param in element.elementProperties:
                typeName = GObject.type_name(param)
                editorClass = None

                if typeName in ("GParamFloat", "GParamDouble"):
                    editorClass = ParamFloatEditor
                elif typeName in ("GParamInt", "GParamInt64", "ParamUInt", 
                    "GParamUInt", "GParamUInt64", "GParamLong", "GParamULong"):
                    editorClass = ParamIntEditor
                elif typeName in ("GParamString", "GParamChar",  "GParamUChar"):
                    editorClass = ParamStringEditor
                elif typeName == "GParamEnum":
                    editorClass = ParamEnumEditor
                elif typeName == "GParamBoolean":
                    editorClass = ParamBooleanEditor
                elif typeName == "ClutterParamSpecColor":
                    editorClass = ParamColorEditor
                # elif typeName == "GParamFlags":
                #   self.addEditor(ParamFlagsEditor(param, element, value))
                else:
                    pass #print typeName

                if editorClass:
                    # Must assign the editor to a variable
                    editor = editorClass(param, element)
                    # element.connect("property-changed", editor.update)
                    self.addEditor(editor)

    def onElementPropertyChanged(self, sender, element, name):
        if self.currentElement == element:
            self.editors[name].update()

    def clear(self):
        self.currentElement = None
        for child in self.grid.get_children():
            child.destroy()
        self.editors = {}


class ParamEditor(object):
    def __init__(self, param, element):
        self.param = param
        self.element = element
        self.value = None

    def updateValue(self):
        self.value = self.element.getProperty(self.param.name)


class ParamStringEditor(ParamEditor):
    def __init__(self, *args, **kwargs):
        super(ParamStringEditor, self).__init__(*args, **kwargs)
        self.trigger = False
        self.widget = Gtk.Entry()
        self.handler = self.widget.connect("changed", self.onChanged)
        self.update()
        self.trigger = True

    def onChanged(self, event):
        self.value = self.widget.get_text()
        self.element.setProperty(self.param.name, self.value, self.trigger)

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        self.widget.set_text(self.value or "")
        self.widget.handler_unblock(self.handler)
        

class ParamBooleanEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamBooleanEditor, self).__init__(*args)
        self.trigger = False
        self.widget = Gtk.ToggleButton()
        self.handler = self.widget.connect("toggled", self.onToggle)
        self.update()
        self.trigger = True
        
    def onToggle(self, button):
        self.value = button.get_active()
        self.toggleText(self.value)
        self.element.setProperty(self.param.name, self.value, self.trigger)
        
    def toggleText(self, value):
        if self.value:
            self.widget.set_label("Yes")
        else:
            self.widget.set_label("No")

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        self.toggleText(self.value)
        self.widget.set_active(self.value)
        self.widget.handler_unblock(self.handler)


class ParamFloatEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamFloatEditor, self).__init__(*args)
        self.trigger = False
        self.widget = Gtk.SpinButton()
        self.widget.set_range(max(-99999999, self.param.minimum), 
            min( 99999999, self.param.maximum))
        self.widget.set_increments(0.1, 1.0)
        self.widget.set_digits(2)
        self.handler = self.widget.connect("value-changed", self.onValueChanged)
        self.update()
        self.trigger = True

    def onValueChanged(self, event):
        self.value = self.widget.get_value()
        self.element.setProperty(self.param.name, self.value, self.trigger)

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        self.widget.set_value(self.value)
        self.widget.handler_unblock(self.handler)


class ParamIntEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamIntEditor, self).__init__(*args)
        self.trigger = False
        self.widget = Gtk.SpinButton()
        self.widget.set_range(max(-99999999, self.param.minimum), 
            min(99999999, self.param.maximum))
        self.widget.set_increments(1, 10)
        self.widget.set_digits(2)
        self.handler = self.widget.connect("value-changed", self.onValueChanged)
        self.update()
        self.trigger = True

    def onValueChanged(self, event):
        self.value = self.widget.get_value()
        self.element.setProperty(self.param.name, self.value, self.trigger)

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        self.widget.set_value(self.value)
        self.widget.handler_unblock(self.handler)


class ParamEnumEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamEnumEditor, self).__init__(*args)
        self.trigger = False
        self.widget = Gtk.ComboBoxText()
        self.enum = {}
        enumValues = self.param.enum_class.__enum_values__
        for _, value in enumValues.iteritems():
            nick = self.convertToTitle(value.value_nick)
            self.enum[nick] = value
            self.widget.append_text(nick)

        self.handler = self.widget.connect("changed", self.onChanged)
        self.update()
        self.trigger = True

    def onChanged(self, event):
        self.value = self.enum[self.convertToTitle(
            self.widget.get_active_text())]
        self.element.setProperty(self.param.name, self.value, self.trigger)

    def convertToTitle(self, text):
        return text.replace("-", " ").title()

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        self.widget.set_active(self.enum.keys().index(self.convertToTitle(
            self.value.value_nick)))
        self.widget.handler_unblock(self.handler)


class ParamColorEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamColorEditor, self).__init__(*args)
        self.trigger = False
        self.widget = Gtk.ColorButton()
        self.widget.set_use_alpha(True)

        self.handler = self.widget.connect("color-set", self.onColorSet)
        self.update()
        self.trigger = True

    def onColorSet(self, event):
        color = self.widget.get_rgba()
        
        actorColor = Clutter.Color()
        actorColor.red   = color.red   * 255.0
        actorColor.green = color.green * 255.0
        actorColor.blue  = color.blue  * 255.0
        actorColor.alpha = color.alpha * 255.0
        
        self.value = actorColor
        self.element.setProperty(self.param.name, self.value)

    def update(self):
        self.widget.handler_block(self.handler)
        self.updateValue()
        actorColor = self.value
        color = Gdk.RGBA()
        color.red   = actorColor.red   / 255.0
        color.green = actorColor.green / 255.0
        color.blue  = actorColor.blue  / 255.0
        color.alpha = actorColor.alpha / 255.0

        self.widget.set_rgba(color)
        self.widget.handler_unblock(self.handler)


class ParamFlagsEditor(ParamEditor):
    def __init__(self, *args):
        super(ParamFlagsEditor, self).__init__(*args)


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
        
        self.treeView.connect("row-activated", self.elementSelected)
        self.treeView.connect("button-press-event" ,self.buttonPressEvent)
        
    def elementSelected(self, widget, path, column):
        root = path.copy()
        path.up()
        modelFilter = self.model.filter_new(path)
        modelFilter.set_visible_func(self.isRowVisible, root)
        self.setModel(modelFilter)
        #self.model.focusOn(path)
        
    def buttonPressEvent(self, widget, event):
        if event.button == 3: # right click
            path = self.treeView.get_path_at_pos(int(event.x), int(event.y))
            if path:
                self.model.deleteElement(path[0])
            # do something with the selected path

    def isRowVisible(self, model, it, root):
        path = model.get_path(it)
        return root.is_ancestor(path) or root == path
    
    def setModel(self, model):
        self.treeView.set_model(model)
        self.model = model
        

class ElementPalette(Gtk.ToolPalette):
    def __init__(self, onElementChanged):
        super(ElementPalette, self).__init__()

        self.onElementChanged = onElementChanged
        
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
            
        self.onElementChanged(self.selectedElement)

    def resetSelected(self):
        self.selectedItem = None
        self.selectedElement = None

class StageView(GtkClutter.Embed):
    def __init__(self, model):
        super(StageView, self).__init__()

        self.elements = {}

        self.stage = self.get_stage()
        self.stage.set_layout_manager(Clutter.BinLayout())
        
        self.stageLayer = Clutter.Actor()
        self.overlayLayer = Clutter.Actor()
        self.stage.add_actor(self.stageLayer)
        self.stage.add_actor(self.overlayLayer)
        
        self.stage.set_background_color(Clutter.Color.new(20, 20, 20, 255))
        
        self.matrix = Cogl.Matrix()
        self.matrix.init_identity()
        #self.matrix.rotate(30, 0, 0, 1)

        self.stageLayer.set_child_transform(self.matrix)
        self.stageLayer.connect("notify::child-transform", self.onTransform)
        self.stageLayer.set_x_expand(True)
        self.stageLayer.set_y_expand(True)
        
        self.stage.connect("scroll-event", self.scroll)
        self.stage.connect("button-press-event", self.mousePress)
        self.stage.connect("button-release-event", self.mouseRelease)
        self.stage.connect("motion-event", self.mouseMove)

        self.resetDrag()
        self.elementClass = None
        self.lastMouseMoveEvent = None
        
        self.setModel(model)
        
    def onTransform(self, actor, param):
        if self.lastMouseMoveEvent:
            self.mouseMove(self.stage, self.lastMouseMoveEvent)
    
    def mousePress(self, actor, event):
        event.x, event.y = int(event.x), int(event.y)
        self.dragging = True
        
        self.dragEventStart = event.x, event.y
        
        if self.elementClass:
            # An item is selected in the associated palette
            self.itemDragging = True
            
            self.parentActor = self.stage.get_actor_at_pos(
                Clutter.PickMode.ALL, event.x, event.y)
            
            # Container checks
            if self.parentActor == self.stage:
                self.parentActor = self.stageLayer
                
            layout = self.parentActor.get_layout_manager()
            
            self.pendingActor = Clutter.Actor()
            self.pendingActor.elementClass = self.elementClass
            self.pendingActor.set_background_color(Clutter.Color.new(random.random() * 255, random.random() * 255, random.random() * 255, 255))
            #self.pendingActor.set_border_color(Clutter.Color.new(255, 255, 255, 255))
            #self.pendingActor.set_border_width(1)
            
            if isinstance(layout, Clutter.FixedLayout):
                self.pendingActor.set_size(0, 0)
                self.pendingActor.hide()
            elif isinstance(layout, Clutter.BinLayout):
                indicator = BinAlignmentIndicator()
                indicator.attachTo(self.parentActor)
                # drawoverlay
            elif isinstance(layout, Clutter.BoxLayout):
                pass
                # drawoverlay
            elif isinstance(layout, Clutter.FlowLayout):
                pass
                # drawoverlay
            
            self.parentActor.add_actor(self.pendingActor)
        elif event.button == 1:
            actor = self.stage.get_actor_at_pos(Clutter.PickMode.ALL, 
                event.x, event.y)
            element = self.elements.keys()[self.elements.values().index(actor)]
            self.model.emit("element-selected", element)
            """
            # Selection box
            self.selectionBox = SelectionBox()
            self.selectionBox.set_position(event.x, event.y)
            self.selectionBox.set_size(0, 0)
            self.selectionBox.hide()
            self.overlayLayer.add_child(self.selectionBox)
            """
    
    def mouseMove(self, actor, event):
        self.lastMouseMoveEvent = event
        event.x, event.y = int(event.x), int(event.y)
        
        if self.dragging:
            if self.itemDragging:
                layout = self.parentActor.get_layout_manager()
                
                position = self.parentActor.get_transformed_position()
                
                inverse = self.matrix.get_inverse()[1]
                x_1, y_1, _, _ = inverse.transform_point(self.dragEventStart[0],
                    self.dragEventStart[1], 0, 0)
                x_2, y_2, _, _ = inverse.transform_point(event.x, event.y, 0, 0)
                x_3, y_3, _, _ = inverse.transform_point(position[0], position[1], 0, 0)
                
                if isinstance(layout, Clutter.FixedLayout):
                    
                    if x_1 == x_2 or y_1 == y_2:
                        self.pendingActor.hide()
                    else:
                        self.pendingActor.show()
                        
                    x_cond = x_2 < x_1
                    y_cond = y_2 < y_1
                    
                    self.pendingActor.set_position(
                        (x_cond * x_2 + (not x_cond) * x_1) - x_3, 
                        (y_cond * y_2 + (not y_cond) * y_1) - y_3)
                    
                    self.pendingActor.set_size(abs(x_2 - x_1), abs(y_2 - y_1))
                elif isinstance(layout, Clutter.BinLayout):
                    pass
                elif isinstance(layout, Clutter.BoxLayout):
                    pass
                elif isinstance(layout, Clutter.FlowLayout):
                    pass
            elif self.selectionBox:
                # Selection box
                if event.x == self.dragEventStart[0] or event.y == self.dragEventStart[1]:
                    self.selectionBox.hide()
                else:
                    self.selectionBox.show()
                    
                x_cond = event.x < self.dragEventStart[0]
                y_cond = event.y < self.dragEventStart[1]
                
                self.selectionBox.set_position(
                    x_cond * event.x + (not x_cond) * self.dragEventStart[0], 
                    y_cond * event.y + (not y_cond) * self.dragEventStart[1])
                
                self.selectionBox.set_size(abs(event.x - self.dragEventStart[0]), 
                    abs(event.y - self.dragEventStart[1]))

    def mouseRelease(self, actor, event):
        if self.itemDragging:
            element = Element(type(self.pendingActor))

            # Copy pendingActor's properties to the element
            element.loadProperties(self.pendingActor)

            self.model.addElement(element, self.elements.keys()[self.elements.values().index(self.parentActor)])
            # Override and set the currently created actor as the proxy
            self.elements[element] = self.pendingActor
        elif self.selectionBox:
            # Process selection
            selectionBox = self.selectionBox
            self.selectionBox.fadeOut(lambda x: 
                                      self.overlayLayer.remove_child(selectionBox))
        self.resetDrag()
    
    def resetDrag(self):
        self.dragging = False
        self.itemDragging = False
        self.dragEventStart = (0, 0)
        self.selectionBox = None
        
    def setElementClass(self, elementClass):
        self.elementClass = elementClass
        #print elementClass
        
    def setModel(self, model):
        self.model = model
        self.model.connect("element-added", self.onElementAdded)
        self.model.connect("element-removed", self.onElementRemoved)
        self.model.connect("element-selected", self.onElementSelected)
        self.model.connect("element-property-changed", 
                           self.onElementPropertyChanged)
        #self.focusOn(model.stage)

        self.elements[self.model.stage] = self.stageLayer
        for childElement in self.model.stage.children:
            self.addElement(childElement)

    def onElementAdded(self, sender, element):
        self.addElement(element)
    
    def onElementRemoved(self, sender, element):
        self.removeElement(element)
    
    def onElementSelected(self, sender, element):
        self.selectElement(element)
    
    def onElementPropertyChanged(self, sender, element, name):
        actor = self.elements[element]
        actor.set_property(name, element.getProperty(name))
    
    def addElement(self, element):
        # This is to only be called by the model

        if element not in self.elements.keys():
            actor = element.createActor()
            self.elements[element.parent].add_actor(actor)
            self.elements[element] = actor

    def removeElement(self, element):
        # This is to only be called by the model
        self.elements[element].parent.remove_actor()
        self.elements[element].destroy()
        self.elements.pop(element)
            
    def selectElement(self, element):
        # This is to only be called by the model
        print element, self.elements[element], " was selected."
            
    def clearStage(self):
        for child in self.stageLayer.get_children():
            child.destroy()
        
    def scroll(self, actor, event):
        factor = 1.1
        if event.direction == Clutter.ScrollDirection.UP:
            self.stageLayer.save_easing_state()
            self.stageLayer.set_easing_duration(150)
            self.stageLayer.set_easing_mode(Clutter.AnimationMode.EASE_OUT_QUAD)
            self.matrix.scale(factor, factor, factor)
            self.stageLayer.set_child_transform(self.matrix)        
            self.stageLayer.restore_easing_state()
        if event.direction == Clutter.ScrollDirection.DOWN:
            factor = 1 / factor
            self.stageLayer.save_easing_state()
            self.stageLayer.set_easing_duration(150)
            self.stageLayer.set_easing_mode(Clutter.AnimationMode.EASE_OUT_QUAD)
            self.matrix.scale(factor, factor, factor)
            self.stageLayer.set_child_transform(self.matrix)        
            self.stageLayer.restore_easing_state()


class BinAlignmentIndicator(Clutter.Actor):
    
    def __init__(self):
        super(BinAlignmentIndicator, self).__init__()
        self.set_color(Clutter.Color.new(255, 0, 100, 200))
        
    def attachTo(self, actor):
        constraint = Clutter.BindConstraint()
        constraint.set_source(actor)
        self.add_constraint(Clutter.BindConstraint)
    
    
class SelectionBox(Clutter.Rectangle):
    
    def __init__(self):
        super(SelectionBox, self).__init__()
        opacity = 0.25

        self.set_color(Clutter.Color.new(100, 100, 100, opacity * 255))
        self.set_border_color(Clutter.Color.new(255, 255, 255, opacity * 255))
        self.set_border_width(1)
        
        self.set_transform(None)
        
    def fadeOut(self, callback):
        self.save_easing_state()
        self.set_easing_duration(75)
        self.set_easing_mode(Clutter.AnimationMode.LINEAR)
        self.set_opacity(0)
        self.restore_easing_state()
        self.get_transition("opacity").connect("completed", callback)