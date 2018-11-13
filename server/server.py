import socket
import os
import hashlib
import buffer

HOST = '127.0.0.1'
PORT = 2345

# Determine Hash Algorithm and Create Hash of File
def getHash(fileName, hashType):
    if hashType == 'sha1':
        hash_sha1 = hashlib.sha1()
        with open(fileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()

    elif hashType == 'sha256':
        hash_sha256 = hashlib.sha256()
        with open(fileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    elif hashType == 'sha512':
        hash_sha512 = hashlib.sha512()
        with open(fileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()

    elif hashType == 'md5':
        hash_md5 = hashlib.md5()
        with open(fileName, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    else:
        return 'Not a valid hashing algorithm'

try:
    os.mkdir('uploads')
except FileExistsError:
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
print("Waiting for a connection.....")

while True:
    # Connect to Server
    conn, addr = s.accept()
    print("Got a connection from ", addr)
    connbuf = buffer.Buffer(conn)

    while True:
        # Get Hash Type
        hash_type = connbuf.get_utf8()
        if not hash_type:
            break
        print('Hash Type: ', hash_type)

        # Get File Type
        file_name = connbuf.get_utf8()
        if not file_name:
            break
        file_name = os.path.join('uploads', file_name)
        print('File Name: ', file_name)

        # Get File Size
        file_size = connbuf.get_utf8()
        file_size = int(file_size)
        print('File Size: ', file_size)

        # Create File
        with open(file_name, 'wb') as f:
            remaining = file_size
            while remaining:
                if remaining >= 4096:
                    chunk_size = 4096
                else:
                    chunk_size = remaining
                chunk = connbuf.get_bytes(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)

            if remaining:
                print('File incomplete: MISSING', remaining, 'BYTES.')
            else:
                print('File received successfully.')
        
        # Send File Hash Back to Client
        file_hash = getHash(file_name, hash_type)
        file_name = os.path.split(file_name)
        connbuf.put_utf8(file_name[1] + ' ' + file_hash)
    
    print('Connection closed.')
    conn.close()