import socket
import os
import buffer

HOST = '127.0.0.1'
PORT = 2345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

with s:
    sbuf = buffer.Buffer(s)

    hash_type = input('Enter hash type: ')

    files = input('Enter file(s) to send: ')
    files_to_send = files.split()

    for file_name in files_to_send:
        print(file_name)
        sbuf.put_utf8(hash_type)
        sbuf.put_utf8(file_name)

        try: 
            file_size = os.path.getsize(file_name)
            sbuf.put_utf8(str(file_size))

            with open(file_name, 'rb') as f:
                sbuf.put_bytes(f.read())
                print('File Sent')

            response = sbuf.get_utf8()
            print(response)

        except FileNotFoundError:
            print('Not a valid file')
            pass
