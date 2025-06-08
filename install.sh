#!/bin/sh
# Simple installer for AnduinOS Updater
set -e
PREFIX=${PREFIX:-/usr/local}

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

# Fix Exec path in .desktop file
sed -i "s|Exec=anduinupdater|Exec=$PREFIX/bin/anduinupdater|g" "$PREFIX/share/applications/AnduinUpdater.desktop"

echo "AnduinOS Updater installed! You can launch it from the menu or by running 'anduinupdater'."
