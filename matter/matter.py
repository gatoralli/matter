from gi.repository import Gtk, Clutter

from window import MainWindow
import elements, catalog

class Application(object):
    def __init__(self):
        # Load configuration
        self.elementCatalog = catalog.ElementCatalog("element-catalog.xml")

        # Element graph
        self.stageModel = elements.StageModel()
        
        # Create default new project
        self.setProject(Project())

        # Initialize GUI
        self.window = MainWindow(self)
        self.window.elementPalette.loadCatalog(self.elementCatalog)
        
    def setProject(self, project):
        self.project = project
        
    def start(self):
        self.window.show_all()

    def new(self, item=None):
        pass

    def open(self, item=None):
        dialog = Gtk.FileChooserDialog("Open", self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        clutterScript = Gtk.FileFilter()
        clutterScript.set_name("ClutterScript (*.json)")
        clutterScript.add_pattern("*.json")
        dialog.add_filter(clutterScript)

        filterText = Gtk.FileFilter()
        filterText.set_name("Text files")
        filterText.add_mime_type("text/plain")
        dialog.add_filter(filterText)

        filterAny = Gtk.FileFilter()
        filterAny.set_name("Any files")
        filterAny.add_pattern("*")
        dialog.add_filter(filterAny)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.setProject(Project(dialog.get_filename()))
        dialog.destroy()

    def save(self, item=None):
        pass

    def saveAs(self, item=None):
        pass

    def quit(self, item=None):
        Gtk.main_quit()


class Project(object):
    def __init__(self, path=None):
        if path:
            self.path = path
            script = Clutter.Script()
            script.load_from_file(self.path)
        else:
            self.name = "Untitled"
            self.path = None