import socket
from struct import pack
import threading
from protocol import *

host      = socket.gethostname()
host_ip   = socket.gethostbyname(host)
port      = 7070 

clients   = set()
rooms = set()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen()
print(f"Listening on {host_ip}:{port}...")

def recv_msg(socket):
     stop_event = threading.Event()

     while not stop_event.is_set():
          packet = recv_message(socket)
          packet = Packet(type=packet[0], username=packet[1].decode(), data=packet[3].decode())
          print(packet)

          if packet.type == Type['JOIN']:
               new_user = User(client_socket, address, packet.username)
               clients.add(new_user)

               users = "Chat joined. Users: " + ', '.join(user.username for user in clients)
               send_message(socket, Type['SERVER'], "", users)
               send_all(Type['SERVER'], packet.username, f"------- User {packet.username} joined -------")

          if packet.type == Type['MESSAGE']:
               send_all(packet.type, packet.username, packet.data)
          
          if packet.type == Type['LEAVE']:
               for c in clients:
                    if c.username == packet.username:
                         send_all(Type['SERVER'], "", f"------- User {packet.username} left -------")
                         c.client.close()
                         clients.remove(c)
                         break

               users = "Users: " + ', '.join(user.username for user in clients)
               send_all(Type['SERVER'], "", users)
               stop_event.set()

def send_all(type: bytes, username: str, data: str):
     for c in clients:
          if c.username == username: continue
          send_message(c.client, type, username, data)

try:
     while True:
          client_socket, address = server_socket.accept()
          print(f"Connected to {address[0]}")

          t = threading.Thread(target=recv_msg, args=(client_socket,))
          t.start()
finally:
     server_socket.close()