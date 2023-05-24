import socket
import _thread
from protocol import *

host_ip   = "192.168.56.1"
port      = 7070 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))

def listen_print_data(client_socket):
     while True:
          packet = recv_message(client_socket)
          if not packet: break

          packet = Packet(type=packet[0], room=packet[1].decode(), username=packet[2].decode(), data=packet[4].decode())

          if packet.type == Type['SERVER']: print(packet.data)
          if packet.type == Type['MESSAGE']: print(f"> {packet.username}: {packet.data}")

try:
     print("Connection enstablished")

     print("Enter room id:")
     room_id = input()

     print("Enter nickname (MAX 8 chars)")
     username = input()
     while len(username) > 8 or len(username) < 3:
          print("Nickname must be maximum 8 characters long and longer than 3")
          username = input()

     send_message(client_socket, Type['JOIN'], room_id, username, "")

     _thread.start_new_thread(listen_print_data, (client_socket,))

     while True:
          msg = input()
          send_message(client_socket, Type['MESSAGE'], room_id, username, msg)
finally:
     print('closing socket')
     send_message(client_socket, Type['LEAVE'], room_id, username, "")
     _thread.exit()
     client_socket.close()