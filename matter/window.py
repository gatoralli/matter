from gi.repository import Gtk

import matter

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

       	self.menuBar = Gtk.MenuBar()
       	self.toolBar = Gtk.Toolbar()
       	self.pane1 = Gtk.Paned()
       	self.pane2 = Gtk.Paned()
       	self.statusBar = Gtk.Statusbar()
       	self.preview = Gtk.Notebook()

       	# Window Options
       	self.set_title("Matter")
        self.set_size_request(800, 600)

       	# Menu Options
       	fileMenuItem = Gtk.MenuItem("File")
       	fileMenu     = Gtk.Menu()
       	exitItem     = Gtk.MenuItem("Exit")
       	exitItem.connect("activate", matter.quit)
       	fileMenuItem.set_submenu(fileMenu)
       	fileMenu.append(exitItem)
       	self.menuBar.append(fileMenuItem)

       	self.preview.append_page(Gtk.Label("Test"), Gtk.Label("Page 1"))
       	self.pane2.pack1(Gtk.Label("Test"))
       	self.pane2.pack2(self.preview)
       	self.pane1.pack1(self.pane2)
       	self.pane1.pack2(Gtk.Label("Test"))

        vbox = Gtk.VBox(False, 4)
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(self.toolBar, False, False, 0)
        vbox.pack_start(self.pane1, True, True, 0)
        vbox.pack_start(self.statusBar, False, False, 0)

        self.add(vbox)

        self.connect("destroy", matter.quit)