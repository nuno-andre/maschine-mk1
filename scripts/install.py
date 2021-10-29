#!/usr/bin/env python3 -u

from platform import system
from shutil import copytree
from pathlib import Path
import stat
import os


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'Maschine_Mk1'


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            dirname = os.path.join(root, name)
            os.chmod(dirname, stat.S_IWRITE)
            os.rmdir(dirname)
    os.chmod(top, stat.S_IWRITE)
    os.rmdir(top)


def find_win_path():
    '''Returns Windows Ableton Live folder.'''
    import winreg

    # also HKCU\SOFTWARE\Ableton\{...}
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
    value = winreg.QueryValue(reg, r'ableton\Shell\open\command')
    path, _ = value.rsplit(' ', 1)
    return Path(path).parents[1]


def find_mac_path():
    '''Returns MacOS Ableton Live folder.'''
    raise NotImplementedError


def install():
    if system() == 'Windows':
        path = find_win_path() / 'Resources'
        print(path)
    elif system() == 'Darwin':
        path = find_mac_path() / 'Contents/App-Resources'
    else:
        raise NotImplementedError

    if not path.exists():
        raise FileNotFoundError(f'{path} does not exist')

    path /= f'MIDI Remote Scripts/{SCRIPT}'

    if path.exists():
        print('Removing previous installation...')
        # TODO: save user settings
        rmtree(path)

    copytree(ROOT / f'src/{SCRIPT}', path)
    print(f'Script installed in: {path}')


if __name__ == '__main__':
    install()
