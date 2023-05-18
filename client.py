import socket
from _thread import *
from protocol import *

host_ip   = "192.168.54.24"
port      = 7070 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))

def listen_print_data(client_socket):
     while True:
          data = client_socket.recv(1024).decode()
          if not data: break
          print(f"{data}")

def send_input_data(client_socket, username):
     while True:
          msg = input()
          send_message(client_socket, Type['MESSAGE'], username, msg)

try:
     print("Connection enstablished")
     print("Enter nickname (MAX 8 chars)")
     username = input()
     if len(username) > 8: pass

     send_message(client_socket, Type['JOIN'], username, "none")

     start_new_thread(listen_print_data, (client_socket,))

     while True:
          msg = input()
          send_message(client_socket, Type['MESSAGE'], username, msg)
finally:
     print('closing socket')
     client_socket.close()