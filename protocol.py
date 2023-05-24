import struct
from typing import Set

Type = {
    'JOIN': b'\x01',
    'LEAVE': b'\x02',
    'MESSAGE': b'\x03',
    'SERVER': b'\x04'
}

class User:
    def __init__(self, client, address, username: str) -> None:
        self.client = client
        self.address = address
        self.username = username

class Packet:
    def __init__(self, type: bytes, room: str, username: str, data: str) -> None:
        self.type = type
        self.room = room
        self.username = username
        self.data = data
    
    def __str__(self) -> str:
        return f"Type: {self.type}, Room: {self.room}, Username: {self.username}, Data: {self.data}"

class Room:
    def __init__(self, id: str, owner: User) -> None:
        self.id = id
        self.owner = owner
        self.members: Set[User] = {owner}
    
    def get_user(self, user: str) -> User:
        for m in self.members:
            if m.username == user: return m

    def add_member(self, member: User) -> None:
        for m in self.members:
            if m.username == member.username: return print("Username already taken")
        self.members.add(member)

    def remove_member(self, member: User) -> None:
        self.members.remove(member)

    def get_users(self) -> str:
        return "Users: " + ', '.join(user.username for user in self.members) 


def send_message(sock, type: bytes, room: str, username: str, data: str):
    hdr_fmt = f"c8s8si{len(data)}s"

    username += ('\0' * (8 - len(username)))
    room += ('\0' * (8 - len(room)))

    packet = struct.pack(hdr_fmt, type, room.encode(), username.encode(), len(data), data.encode())
    send_length(sock, packet)

def recv_message(sock):
    data = recv_length(sock)
    message_length = int.from_bytes(data[16:21], byteorder='big', signed=False)

    hdr_fmt = f"c8s8si{message_length}s"
    return struct.unpack(hdr_fmt, data)

def send_length(sock, data):
    length = len(data)
    if length >= 125000 : return print("Packet too big to be sent (MAX 1Mb)") 
    sock.send(struct.pack('!I', length))
    sock.send(data)

def recv_length(sock):
    lengthbuf = sock.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    return sock.recv(length)