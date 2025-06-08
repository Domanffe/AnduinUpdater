import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from anduin_updater.apt import check_apt_updates

class UpdaterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="AnduinOS Updater")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.status_label = Gtk.Label(label="Нажмите 'Проверить обновления'")
        vbox.pack_start(self.status_label, False, False, 0)

        self.update_list = Gtk.TextView()
        self.update_list.set_editable(False)
        vbox.pack_start(self.update_list, True, True, 0)

        check_button = Gtk.Button(label="Проверить обновления")
        check_button.connect("clicked", self.on_check_updates)
        vbox.pack_start(check_button, False, False, 0)

    def on_check_updates(self, widget):
        self.status_label.set_text("Проверка...")
        updates = check_apt_updates()
        buf = self.update_list.get_buffer()
        if updates:
            buf.set_text("\n".join(updates))
            self.status_label.set_text(f"Найдено обновлений: {len(updates)}")
        else:
            buf.set_text("Обновлений не найдено.")
            self.status_label.set_text("Система обновлена.")
