# AnduinOS Updater

AnduinOS Updater is a GTK-based graphical tool for checking and installing updates on AnduinOS (Ubuntu-based) systems. It supports APT, Flatpak, and system upgrades via do_anduinos_upgrade.

## Features
- Check for APT/DEB package updates
- Check for Flatpak updates
- One-click system upgrade (APT/DEB)
- One-click AnduinOS upgrade (do_anduinos_upgrade)
- Multilanguage support (English, Russian)
- Simple settings dialog (language selection)
- Modern GTK3 interface

## Requirements
- Python 3
- PyGObject (GTK3 bindings)
- APT, Flatpak, pkexec, do_anduinos_upgrade (for full functionality)

## Installation
1. Install dependencies:
   ```sh
   sudo apt update
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 flatpak
   pip install --user pygobject
   ```
2. (Optional) Copy `AnduinUpdater.desktop` to `~/.local/share/applications/` for menu integration.

## Usage
Run the application:
```sh
python3 main.py
```
Or launch from your desktop menu if you installed the .desktop file.

## License
GPL-3.0
