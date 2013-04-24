from gi.repository import Gtk, GtkClutter

from window import MainWindow

if __name__ == "__main__":
    GtkClutter.init([])

    mainWindow = MainWindow()
    mainWindow.show_all()

    Gtk.main()
