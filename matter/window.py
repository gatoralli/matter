from gi.repository import Gtk, GtkClutter, Clutter
from widgets import PropertiesEditor, OutlineView, ElementPalette, StageView

import matter

class MainWindow(Gtk.Window):
    def __init__(self, application):
        super(MainWindow, self).__init__()

        self.application = application

        self.menuBar = Gtk.MenuBar()
        self.toolBar = Gtk.Toolbar()
        self.pane1 = Gtk.Paned()
        self.pane2 = Gtk.Paned()
        self.pane3 = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.elementPalette = ElementPalette(self.elementChanged)
        self.statusBar = Gtk.Statusbar()
        self.outlineView = OutlineView(self.application.stageModel)
        self.preview = Gtk.Notebook()
        self.stageView = StageView(self.application.stageModel)
        self.propertiesEditor = PropertiesEditor(self.application.stageModel)
        
        # Window Options
        self.set_title("Matter")
        self.set_size_request(800, 600)
        self.pane1.set_margin_top(5)
        self.pane1.set_margin_bottom(5)
        self.pane1.set_margin_left(5)
        self.pane1.set_margin_right(5)

        # Menu Options
        fileMenuItem = Gtk.MenuItem("File")
        fileMenu = Gtk.Menu()
        fileMenuItem.set_submenu(fileMenu)

        newItem = Gtk.MenuItem("New")
        newItem.connect("activate", application.new)
        fileMenu.add(newItem)

        openItem = Gtk.MenuItem("Open")
        openItem.connect("activate", application.open)
        fileMenu.add(openItem)

        saveItem = Gtk.MenuItem("Save")
        saveItem.connect("activate", application.save)
        fileMenu.add(saveItem)

        saveAsItem = Gtk.MenuItem("Save As")
        saveAsItem.connect("activate", application.saveAs)
        fileMenu.add(saveAsItem)

        exitItem = Gtk.MenuItem("Exit")
        exitItem.connect("activate", application.quit)
        fileMenu.add(exitItem)

        self.menuBar.add(fileMenuItem)


        helpMenuItem = Gtk.MenuItem("Help")
        helpMenu     = Gtk.Menu()
        helpMenuItem.set_submenu(helpMenu)

        aboutItem    = Gtk.MenuItem("About")
        aboutItem.connect("activate", application.quit)
        helpMenu.add(aboutItem)

        self.menuBar.add(helpMenuItem)


        fr = Gtk.Frame()
        fr.add(self.stageView)
        self.preview.append_page(fr, Gtk.Label("Test"))

        self.pane3.pack1(self.outlineView)
        self.pane3.pack2(self.propertiesEditor)
        self.pane2.pack1(self.elementPalette)
        self.pane2.pack2(self.preview)
        self.pane1.pack1(self.pane2)
        self.pane1.pack2(self.pane3)

        self.pane1.set_position(600)
        self.pane2.set_position(150)
        self.pane3.set_position(200)

        vbox = Gtk.VBox(False, 4)
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(self.toolBar, False, False, 0)
        vbox.pack_start(self.pane1, True, True, 0)
        vbox.pack_start(self.statusBar, False, False, 0)

        self.add(vbox)

        self.connect("destroy", self.application.quit)

    def elementChanged(self, element):
        self.stageView.setElementClass(element)