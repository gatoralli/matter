from gi.repository import Gtk

from window import MainWindow
import elements, catalog

class Application(object):
    def __init__(self):
        # Load configuration
        self.elementCatalog = catalog.ElementCatalog("element-catalog.xml")

        # Initialize GUI
        self.window = MainWindow(self)
        self.window.elementPalette.loadCatalog(self.elementCatalog)
        
    def start(self):
        self.window.show_all()

    def quit(self, item):
        Gtk.main_quit()
