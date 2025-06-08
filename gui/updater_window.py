import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from anduin_updater.apt import check_all_updates, do_apt_upgrade, do_anduinos_upgrade, load_settings, save_settings, tr, check_self_update
import os
import sys

class UpdaterWindow(Gtk.Window):
    def __init__(self):
        self.settings = load_settings()
        Gtk.Window.__init__(self, title=tr('title', self.settings))
        self.set_border_width(10)
        self.set_default_size(500, 500)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.status_label = Gtk.Label(label=tr('check_updates', self.settings))
        vbox.pack_start(self.status_label, False, False, 0)

        self.self_update_label = Gtk.Label(label="")
        vbox.pack_start(self.self_update_label, False, False, 0)

        self.update_list = Gtk.TextView()
        self.update_list.set_editable(False)
        vbox.pack_start(self.update_list, True, True, 0)

        check_button = Gtk.Button(label=tr('check_updates', self.settings))
        check_button.connect("clicked", self.on_check_updates)
        vbox.pack_start(check_button, False, False, 0)

        upgrade_button = Gtk.Button(label=tr('upgrade_all', self.settings))
        upgrade_button.connect("clicked", self.on_upgrade_all)
        vbox.pack_start(upgrade_button, False, False, 0)

        os_upgrade_button = Gtk.Button(label=tr('os_upgrade', self.settings))
        os_upgrade_button.connect("clicked", self.on_os_upgrade)
        vbox.pack_start(os_upgrade_button, False, False, 0)

        settings_button = Gtk.Button(label=tr('settings', self.settings))
        settings_button.connect("clicked", self.on_settings)
        vbox.pack_start(settings_button, False, False, 0)

    def on_check_updates(self, widget):
        self.status_label.set_text(tr('status_check', self.settings))
        updates = check_all_updates()
        buf = self.update_list.get_buffer()
        if updates:
            buf.set_text("\n".join(updates))
            self.status_label.set_text(tr('status_found', self.settings).format(count=len(updates)))
        else:
            buf.set_text(tr('status_none', self.settings))
            self.status_label.set_text(tr('status_up_to_date', self.settings))
        self_update = check_self_update()
        if self_update:
            self.self_update_label.set_text(self_update)
        else:
            self.self_update_label.set_text("")

    def on_upgrade_all(self, widget):
        self.status_label.set_text(tr('status_upgrade', self.settings))
        buf = self.update_list.get_buffer()
        buf.set_text("")
        Gtk.main_iteration_do(False)
        result = do_apt_upgrade()
        buf.set_text(result)
        self.status_label.set_text(tr('status_upgrade_done', self.settings))

    def on_os_upgrade(self, widget):
        self.status_label.set_text(tr('status_os_upgrade', self.settings))
        buf = self.update_list.get_buffer()
        buf.set_text("")
        Gtk.main_iteration_do(False)
        result = do_anduinos_upgrade()
        buf.set_text(result)
        self.status_label.set_text(tr('status_os_upgrade_done', self.settings))

    def on_settings(self, widget):
        dialog = Gtk.Dialog(tr('settings', self.settings), self, 0)
        box = dialog.get_content_area()
        lang_label = Gtk.Label(label=tr('language', self.settings))
        box.add(lang_label)
        lang_combo = Gtk.ComboBoxText()
        lang_combo.append('auto', 'Auto')
        lang_combo.append('ru', 'Русский')
        lang_combo.append('en', 'English')
        lang_combo.set_active_id(self.settings.get('language', 'auto'))
        box.add(lang_combo)
        dialog.add_button(tr('save', self.settings), Gtk.ResponseType.OK)
        dialog.add_button(tr('cancel', self.settings), Gtk.ResponseType.CANCEL)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.settings['language'] = lang_combo.get_active_id()
            save_settings(self.settings)
            self.destroy()
            Gtk.main_quit()
            os.execl(sys.executable, sys.executable, *sys.argv)
        dialog.destroy()
