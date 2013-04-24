from gi.repository import Gtk, GtkClutter, Clutter
from widgets import PropertiesEditor, OutlineView

import matter

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

       	self.menuBar = Gtk.MenuBar()
       	self.toolBar = Gtk.Toolbar()
       	self.pane1 = Gtk.Paned()
       	self.pane2 = Gtk.Paned()
        self.pane3 = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
       	self.statusBar = Gtk.Statusbar()
        self.propertiesEditor = PropertiesEditor()
        self.outlineView = OutlineView()
       	self.preview = Gtk.Notebook()
        self.tempStage = GtkClutter.Embed()
        self.tempStage.get_stage().set_background_color(Clutter.Color.new(20, 20, 20, 255))
       	# Window Options
       	self.set_title("Matter")
        self.set_size_request(800, 600)
        self.pane1.set_margin_top(5)
        self.pane1.set_margin_bottom(5)
        self.pane1.set_margin_left(5)
        self.pane1.set_margin_right(5)
       	# Menu Options
       	fileMenuItem = Gtk.MenuItem("File")
       	fileMenu     = Gtk.Menu()
       	exitItem     = Gtk.MenuItem("Exit")
       	exitItem.connect("activate", matter.quit)
       	fileMenuItem.set_submenu(fileMenu)
       	fileMenu.append(exitItem)
       	self.menuBar.append(fileMenuItem)

       	self.preview.append_page(self.tempStage, Gtk.Label("Page 1"))
       	self.pane3.pack1(self.outlineView)
        self.pane3.pack2(self.propertiesEditor)
        self.pane2.pack1(Gtk.Label("Test"))
       	self.pane2.pack2(self.preview)
       	self.pane1.pack1(self.pane2)
       	self.pane1.pack2(self.pane3)

        vbox = Gtk.VBox(False, 4)
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(self.toolBar, False, False, 0)
        vbox.pack_start(self.pane1, True, True, 0)
        vbox.pack_start(self.statusBar, False, False, 0)

        self.add(vbox)

        self.connect("destroy", matter.quit)
