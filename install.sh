#!/bin/sh
# Simple installer for AnduinOS Updater
set -e
PREFIX=${PREFIX:-/usr/local}

# Show license and ask for confirmation
if [ -f LICENSE ]; then
    echo "\n================ LICENSE (GPL-3.0) ================\n"
    head -40 LICENSE
    echo "..."
    echo "\nBy installing, you accept the license above. Continue? [y/N]"
    read ans
    case $ans in
        [Yy]*) ;;
        *) echo "Installation cancelled."; exit 1;;
    esac
fi

# Copy main files
install -Dm755 anduinupdater "$PREFIX/bin/anduinupdater"
install -Dm644 AnduinUpdater.desktop "$PREFIX/share/applications/AnduinUpdater.desktop"
install -Dm644 LICENSE "$PREFIX/share/doc/anduinupdater/LICENSE"
install -Dm644 README.md "$PREFIX/share/doc/anduinupdater/README.md"

# Copy Python sources
mkdir -p "$PREFIX/share/anduinupdater/anduin_updater"
cp -r anduin_updater "$PREFIX/share/anduinupdater/"
cp -r gui "$PREFIX/share/anduinupdater/"
cp main.py "$PREFIX/share/anduinupdater/"
cp VERSION "$PREFIX/share/anduinupdater/"

sed -i "s|Exec=anduinupdater|Exec=$PREFIX/bin/anduinupdater|g" "$PREFIX/share/applications/AnduinUpdater.desktop"

echo "AnduinOS Updater installed! You can launch it from the menu or by running 'anduinupdater'."
