from gi.repository import Gtk, GtkClutter
import matter

if __name__ == "__main__":
    GtkClutter.init([])

    application = matter.Application()
    application.start()

    Gtk.main()
