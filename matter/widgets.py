from gi.repository import Gtk

class PropertiesEditor(Gtk.Frame):
    def __init__(self):
        super(PropertiesEditor, self).__init__()

        self.set_label("Properties")
        # General tab with background color
        self.notebook = Gtk.Notebook()
        self.notebook.append_page(Gtk.Label("General"), Gtk.Label("General"))
        self.add(self.notebook)

class OutlineView(Gtk.Frame):
    def __init__(self):
        super(OutlineView, self).__init__()

        self.set_label("Outline")
        
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_shadow_type(Gtk.ShadowType.IN)
        self.treeView = Gtk.TreeView()
        
        scrolledWindow.add(self.treeView)
        self.add(scrolledWindow)