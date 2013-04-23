from gi.repository import Gtk

from window import MainWindow

if __name__ == "__main__":
    mainWindow = MainWindow()
    mainWindow.show_all()
    Gtk.main()
