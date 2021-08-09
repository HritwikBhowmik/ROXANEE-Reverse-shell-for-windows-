

gen = open('ROXANA.exe', 'rb')
byte = gen.read()

with open('ROXANA.box', 'wb') as enc:
    enc.write(byte)
    enc.close()