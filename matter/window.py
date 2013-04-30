from gi.repository import Gtk, GtkClutter, Clutter
from widgets import PropertiesEditor, OutlineView, ElementPalette, ActorPreview

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
        self.elementPalette = ElementPalette()
        self.elementPalette.connect("element-changed", self.elementChanged)
        self.statusBar = Gtk.Statusbar()
        self.propertiesEditor = PropertiesEditor()
        self.outlineView = OutlineView(self.application.elementGraph)
        self.preview = Gtk.Notebook()
        self.embed = ActorPreview()
        
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
        exitItem.connect("activate", application.quit)
        fileMenuItem.set_submenu(fileMenu)
        fileMenu.append(exitItem)
        self.menuBar.append(fileMenuItem)

        fr = Gtk.Frame()
        fr.add(self.embed)

        self.preview.append_page(fr, Gtk.Label("Test"))
        self.pane3.pack1(self.outlineView)
        self.pane3.pack2(self.propertiesEditor)
        self.pane2.pack1(self.elementPalette)
        self.pane2.pack2(self.preview)
        self.pane1.pack1(self.pane2)
        self.pane1.pack2(self.pane3)

        vbox = Gtk.VBox(False, 4)
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(self.toolBar, False, False, 0)
        vbox.pack_start(self.pane1, True, True, 0)
        vbox.pack_start(self.statusBar, False, False, 0)

        self.add(vbox)

        self.connect("destroy", self.application.quit)

    def elementChanged(self, item, element):
        self.embed.setElementClass(element)