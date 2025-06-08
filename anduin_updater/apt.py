import subprocess
import shutil
import os
import json
import locale

SETTINGS_PATH = os.path.expanduser('~/.anduinupdater_settings.json')

DEFAULT_SETTINGS = {
    'language': 'auto',
}

LANGS = {
    'ru': {
        'title': 'AnduinOS Апдейтер',
        'check_updates': 'Проверить обновления',
        'upgrade_all': 'Обновить всё',
        'os_upgrade': 'Обновить AnduinOS',
        'status_check': 'Проверка...',
        'status_found': 'Найдено обновлений: {count}',
        'status_none': 'Обновлений не найдено.',
        'status_up_to_date': 'Система обновлена.',
        'status_upgrade': 'Обновление...',
        'status_upgrade_done': 'Обновление завершено',
        'status_os_upgrade': 'Обновление AnduinOS...',
        'status_os_upgrade_done': 'Обновление AnduinOS завершено',
        'settings': 'Настройки',
        'language': 'Язык',
        'save': 'Сохранить',
        'cancel': 'Отмена',
    },
    'en': {
        'title': 'AnduinOS Updater',
        'check_updates': 'Check for updates',
        'upgrade_all': 'Upgrade all',
        'os_upgrade': 'Upgrade AnduinOS',
        'status_check': 'Checking...',
        'status_found': 'Updates found: {count}',
        'status_none': 'No updates found.',
        'status_up_to_date': 'System is up to date.',
        'status_upgrade': 'Upgrading...',
        'status_upgrade_done': 'Upgrade complete',
        'status_os_upgrade': 'Upgrading AnduinOS...',
        'status_os_upgrade_done': 'AnduinOS upgrade complete',
        'settings': 'Settings',
        'language': 'Language',
        'save': 'Save',
        'cancel': 'Cancel',
    }
}

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

def get_lang(settings):
    lang = settings.get('language', 'auto')
    if lang == 'auto':
        sys_lang = locale.getdefaultlocale()[0]
        if sys_lang and sys_lang.startswith('ru'):
            return 'ru'
        return 'en'
    return lang if lang in LANGS else 'en'

def tr(key, settings=None):
    if settings is None:
        settings = load_settings()
    lang = get_lang(settings)
    return LANGS[lang].get(key, key)

def check_apt_updates():
    """Check for APT/DEB package updates. Returns a list of update lines or error messages."""
    apt_path = shutil.which('apt') or '/usr/bin/apt'
    apt_get_path = shutil.which('apt-get') or '/usr/bin/apt-get'
    if not (os.path.exists(apt_path) or os.path.exists(apt_get_path)):
        return ['Error: apt or apt-get not found']
    try:
        if os.path.exists(apt_path):
            cmd = [apt_path, 'list', '--upgradeable']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 and 'permission denied' in result.stderr.lower():
                return ['Error: insufficient permissions. Run with sudo or pkexec.']
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1:]
            return []
        elif os.path.exists(apt_get_path):
            cmd = [apt_get_path, '-s', 'upgrade']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 and 'permission denied' in result.stderr.lower():
                return ['Error: insufficient permissions. Run with sudo or pkexec.']
            lines = result.stdout.strip().split('\n')
            updates = [line for line in lines if line.strip().startswith('Inst')]
            return updates
        else:
            return ['Error: apt or apt-get not found']
    except Exception as e:
        return [f'Error: {e}']

def check_flatpak_updates():
    """Check for Flatpak updates. Returns a list of update lines or error messages."""
    flatpak_path = shutil.which('flatpak') or '/usr/bin/flatpak'
    if not os.path.exists(flatpak_path):
        return []
    try:
        cmd = [flatpak_path, 'remote-ls', '--updates']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return [f'Flatpak error: {result.stderr.strip()}']
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            return lines[1:]
        return []
    except Exception as e:
        return [f'Flatpak error: {e}']

def check_all_updates():
    """Check for both APT/DEB and Flatpak updates."""
    updates = []
    apt_updates = check_apt_updates()
    if apt_updates:
        updates.append('APT/DEB:')
        updates.extend(apt_updates)
    flatpak_updates = check_flatpak_updates()
    if flatpak_updates:
        updates.append('\nFlatpak:')
        updates.extend(flatpak_updates)
    return updates

def do_apt_upgrade():
    """Run apt upgrade or apt-get upgrade with pkexec. Returns output or error message."""
    apt_path = shutil.which('apt') or '/usr/bin/apt'
    apt_get_path = shutil.which('apt-get') or '/usr/bin/apt-get'
    if os.path.exists(apt_path):
        cmd = ['pkexec', apt_path, 'upgrade', '-y']
    elif os.path.exists(apt_get_path):
        cmd = ['pkexec', apt_get_path, 'upgrade', '-y']
    else:
        return 'Error: apt or apt-get not found'
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip() or 'Upgrade complete.'
        else:
            return f'Upgrade error: {result.stderr.strip()}'
    except Exception as e:
        return f'Upgrade error: {e}'

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
                local_version = '0.2'
            if latest_version and latest_version != local_version:
                return f'New version available: {latest_version}\nDownload: {data.get("html_url")}'
            else:
                return None
    except Exception as e:
        return None
