# Custom Buffer Class
class Buffer:
    def __init__(self,s):
        self.sock = s
        self.buffer = b''

    # Get Bytes from TCP Stream
    def get_bytes(self,n):
        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data
        
        data,self.buffer = self.buffer[:n],self.buffer[n:]
        return data

    # Send Bytes to TCP Stream
    def put_bytes(self,data):
        self.sock.sendall(data)

    # Get UTF-8 from TCP Stream by Stopping at NULL
    def get_utf8(self):
        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data
        
        data,_,self.buffer = self.buffer.partition(b'\x00')
        return data.decode()

    # Send UTF-* to TCP Stream
    def put_utf8(self,s):
        if '\x00' in s:
            raise ValueError('string contains delimiter(null)')
        self.sock.sendall(s.encode() + b'\x00')