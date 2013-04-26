from gi.repository import Gtk

from window import MainWindow
import elements

class Application(object):
    def __init__(self):
        # Load configuration
        self.elementConfig = elements.getConfig()

        # Initialize GUI
        self.window = MainWindow(self)
        self.window.elementPalette.applyConfig(self.elementConfig)
        
    def start(self):
        self.window.show_all()

    def quit(self, item):
        Gtk.main_quit()
