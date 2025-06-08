# AnduinUpdater

Апдейтер для AnduinOS (Ubuntu-based) с GTK GUI.

## Структура
- anduin_updater/ — логика проверки и установки обновлений
- gui/ — GTK-интерфейс
- main.py — точка входа

## Зависимости
- Python 3
- PyGObject (GTK)

## Установка зависимостей
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
pip install pygobject

## Запуск
python3 main.py
