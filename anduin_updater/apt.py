import subprocess
import shutil
import os

def check_apt_updates():
    """Проверяет наличие обновлений через apt или apt-get. Если не хватает прав — сообщает об этом."""
    apt_path = shutil.which('apt') or '/usr/bin/apt'
    apt_get_path = shutil.which('apt-get') or '/usr/bin/apt-get'
    if not (os.path.exists(apt_path) or os.path.exists(apt_get_path)):
        return ['Ошибка: не найден apt или apt-get']
    try:
        if os.path.exists(apt_path):
            cmd = [apt_path, 'list', '--upgradeable']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 and 'permission denied' in result.stderr.lower():
                return ['Ошибка: недостаточно прав. Запустите программу с sudo или через pkexec.']
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1:]
            return []
        elif os.path.exists(apt_get_path):
            cmd = [apt_get_path, '-s', 'upgrade']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 and 'permission denied' in result.stderr.lower():
                return ['Ошибка: недостаточно прав. Запустите программу с sudo или через pkexec.']
            lines = result.stdout.strip().split('\n')
            updates = [line for line in lines if line.strip().startswith('Inst')]
            return updates
        else:
            return ['Ошибка: не найден apt или apt-get']
    except Exception as e:
        return [f'Ошибка: {e}']
