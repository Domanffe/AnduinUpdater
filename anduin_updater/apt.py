import subprocess
import shutil
import os
import json
import locale

def load_settings():
    SETTINGS_PATH = os.path.expanduser('~/.anduinupdater_settings.json')
    DEFAULT_SETTINGS = {'language': 'auto'}
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    SETTINGS_PATH = os.path.expanduser('~/.anduinupdater_settings.json')
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

def get_lang(settings):
    LANGS = {
        'ru': {'title': 'AnduinOS Апдейтер', 'os_upgrade': 'Обновить AnduinOS', 'status_os_upgrade': 'Обновление AnduinOS...', 'status_os_upgrade_done': 'Обновление AnduinOS завершено', 'settings': 'Настройки', 'language': 'Язык', 'save': 'Сохранить', 'cancel': 'Отмена'},
        'en': {'title': 'AnduinOS Updater', 'os_upgrade': 'Upgrade AnduinOS', 'status_os_upgrade': 'Upgrading AnduinOS...', 'status_os_upgrade_done': 'AnduinOS upgrade complete', 'settings': 'Settings', 'language': 'Language', 'save': 'Save', 'cancel': 'Cancel'}
    }
    lang = settings.get('language', 'auto')
    if lang == 'auto':
        sys_lang = locale.getdefaultlocale()[0]
        if sys_lang and sys_lang.startswith('ru'):
            return 'ru'
        return 'en'
    return lang if lang in LANGS else 'en'

def tr(key, settings=None):
    LANGS = {
        'ru': {'title': 'AnduinOS Апдейтер', 'os_upgrade': 'Обновить AnduinOS', 'status_os_upgrade': 'Обновление AnduinOS...', 'status_os_upgrade_done': 'Обновление AnduinOS завершено', 'settings': 'Настройки', 'language': 'Язык', 'save': 'Сохранить', 'cancel': 'Отмена'},
        'en': {'title': 'AnduinOS Updater', 'os_upgrade': 'Upgrade AnduinOS', 'status_os_upgrade': 'Upgrading AnduinOS...', 'status_os_upgrade_done': 'AnduinOS upgrade complete', 'settings': 'Settings', 'language': 'Language', 'save': 'Save', 'cancel': 'Cancel'}
    }
    if settings is None:
        settings = load_settings()
    lang = get_lang(settings)
    return LANGS[lang].get(key, key)

def do_anduinos_upgrade():
    """Run do_anduinos_upgrade with pkexec. Returns output or error message."""
    anduinos_path = shutil.which('do_anduinos_upgrade') or '/usr/bin/do_anduinos_upgrade'
    if not os.path.exists(anduinos_path):
        return 'Error: do_anduinos_upgrade not found'
    try:
        cmd = ['pkexec', anduinos_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip() or 'AnduinOS upgrade complete.'
        else:
            return f'AnduinOS upgrade error: {result.stderr.strip()}'
    except Exception as e:
        return f'AnduinOS upgrade error: {e}'

def check_self_update():
    """Check for new version of AnduinOS Updater on GitHub."""
    import urllib.request
    import json
    GITHUB_API = "https://api.github.com/repos/Domanffe/AnduinUpdater/releases/latest"
    try:
        with urllib.request.urlopen(GITHUB_API, timeout=5) as resp:
            data = json.load(resp)
            latest_version = data.get('tag_name')
            local_version = None
            version_path = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
            if os.path.exists(version_path):
                with open(version_path) as f:
                    local_version = f.read().strip()
            else:
                local_version = '0.3'
            if latest_version and latest_version.lstrip('v') != local_version.lstrip('v'):
                return f'New version available: {latest_version}\nDownload: {data.get("html_url")}'
            else:
                return None
    except Exception:
        return None
