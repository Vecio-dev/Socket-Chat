import socket
from struct import pack
import threading
from protocol import *

host      = socket.gethostname()
host_ip   = socket.gethostbyname(host)
port      = 7070 
clients   = set()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen()
print(f"Listening on {host_ip}:{port}...")

def recv_msg(socket):
     while True:
          packet = recv_message(socket)
          # (b'\x03', b'vegeta\x00\x00', 4, b'ciao')
          print(packet)

          if packet[0] == Type['JOIN']:
               new_user = User(client_socket, address, packet[1])
               clients.add(new_user)

               users = "Chat joined. Users: " + ', '.join(user.username.decode() for user in clients)
               socket.send(users.encode())

               join_message = f"------- User {packet[1].decode()} joined -------"
               send_all(packet[1], join_message)

          if packet[0] == Type['MESSAGE']:
               message = packet[1].decode() + ": " + packet[3].decode()
               send_all(packet[1], message)

def send_all(username, message):
     for c in clients:
          if c.username == username: continue
          c.client.sendall(message.encode())

try:
     while True:
          client_socket, address = server_socket.accept()
          print(f"Connected to {address[0]}")

          t = threading.Thread(target=recv_msg, args=(client_socket,))
          t.start()
finally:
     server_socket.close()