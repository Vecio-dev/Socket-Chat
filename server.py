import socket
import threading
from protocol import *

host      = socket.gethostname()
host_ip   = socket.gethostbyname(host)
port      = 7070 

rooms     = set()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen()
print(f"Listening on {host_ip}:{port}...")

def recv_msg(socket):
     stop_event = threading.Event()

     while not stop_event.is_set():
          packet = recv_message(socket)
          packet = Packet(type=packet[0], room=packet[1].decode(), username=packet[2].decode(), data=packet[4].decode())
          print(packet)

          if packet.type == Type['JOIN']:
               new_user = User(client_socket, address, packet.username)

               this_room = get_room(packet.room)
               if this_room == None:
                    this_room = Room(packet.room, new_user)
                    rooms.add(this_room)
               else: this_room.add_member(new_user)         

               users = this_room.get_users()
               send_message(socket, Type['SERVER'], packet.room, "", users)
               send_all(Type['SERVER'], packet.room, packet.username, f"------- User {packet.username} joined -------")

          if packet.type == Type['MESSAGE']:
               send_all(packet.type, packet.room, packet.username, packet.data)
          
          if packet.type == Type['LEAVE']:
               this_room = get_room(packet.room)
               for user in this_room.members:
                    if user.username == packet.username:
                         send_all(Type['SERVER'], packet.room, "", f"------- User {packet.username} left -------")
                         user.client.close()
                         this_room.remove_member(user)
                         break
               
               users = this_room.get_users()
               send_all(Type['SERVER'], packet.room, "", users)
               stop_event.set()

def send_all(type: bytes, room: str, username: str, data: str):
     r = get_room(room)
     for user in r.members:
          if user.username == username: continue
          send_message(user.client, type, room, username, data)

def get_room(id: str):
     for room in rooms:
        if room.id == id:
            return room
     return None

try:
     while True:
          client_socket, address = server_socket.accept()
          print(f"Connected to {address[0]}")

          t = threading.Thread(target=recv_msg, args=(client_socket,))
          t.start()
finally:
     server_socket.close()