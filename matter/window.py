from gi.repository import Gtk

import matter

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()

       	self.menuBar = Gtk.MenuBar()

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

        vbox = Gtk.VBox(False, 2)
        vbox.pack_start(self.menuBar, False, False, 0)

        self.add(vbox)

        self.connect("destroy", matter.quit)
        # self.set_position(Gtk.WindowPosition.CENTER)