import struct

Type = {
    'JOIN': b'\x01',
    'LEAVE': b'\x02',
    'MESSAGE': b'\x03'
}

class User:
    def __init__(self, client, address, username):
        self.client = client
        self.address = address
        self.username = username

def send_message(sock, type, username, data):
    hdr_fmt = f"c8si{len(data)}s"

    # Username resolve
    username += ('\0' * (8 - len(username)))

    packet = struct.pack(hdr_fmt, type, username.encode(), len(data), data.encode())
    send_length(sock, packet)

# 1 8 4 N
def recv_message(sock):
    data = recv_length(sock)

    #data = sock.recv(1024)
    message_length = int.from_bytes(data[8:13], byteorder='big', signed=False)
    
    hdr_fmt = f"c8si{message_length}s"
    return struct.unpack(hdr_fmt, data)

def send_length(sock, data):
    length = len(data)
    sock.send(struct.pack('!I', length))
    sock.send(data)

def recv_length(sock):
    lengthbuf = sock.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    return sock.recv(length)