# Socket Chat

## Protocol
I defined a protocol to control the communication between the client and the server.


# Packet Format:
The packet format consists of a header and a data section. The header contains the Type, Username, and Length fields, while the data section holds the actual data being transmitted.

The header is structured as a table with the following columns: Type, Username, Length, and Data. Each column represents a specific field in the packet.

| Type | Username | Length | Data |
|------|----------|--------|------|


#
**Type:**  
The `Type` field is 1 byte in size and specifies the type of the message being sent. It is implemented using the Type dictionary, which maps the message types to their corresponding binary values. The available message types are:
```py
Type = {
    'JOIN': b'\x01',
    'LEAVE': b'\x02',
    'MESSAGE': b'\x03'
}
```
<li>`JOIN`: This message is emitted when a user joins the chat.</li>
<li>`LEAVE`: This message is emitted when a userleaves the chat.</li>
<li>`MESSAGE`: This message is emitted when a usersends a message.</li>

#
**Username:**  
The `Username` field is 8 bytes in size and represents the username of the sender. In each packet, the username is normalized to a length of 8 bytes. If the username is shorter than 8 bytes, null bytes ('\0') are appended to fill the remaining space.
```py
username += ('\0' * (8 - len(username)))
```
#
**Length:**  
The `Length` field is 4 bytes in size and denotes the length of the `Data` field. It is an integer value that specifies the number of bytes in the data section.
#
**Data:**  
The `Data` field is a character array of variable length and contains the actual data being transmitted. The length of the `Data` field is determined by the value in the `Length` field.
#

# Send/Recieve Methods
The provided code includes two functions: send_message() and recv_message(). These functions handle the sending and receiving of packets according to the defined protocol.  

The `send_message()` function is responsible for sending a packet over a socket connection. It takes the following parameters: `sock` (the socket connection), `type` (the message type), `username` (the sender's username), and `data` (the message data).
```py
def send_message(sock, type, username, data):
    hdr_fmt = f"c8si{len(data)}s"

    # Username resolve
    username += ('\0' * (8 - len(username)))

    packet = struct.pack(hdr_fmt, type, username.encode(), len(data), data.encode())
    send_length(sock, packet)
```
The function first defines the header format using the `hdr_fmt` string, which specifies the format of the packet fields using the `struct` module. The `hdr_fmt` string is constructed dynamically based on the length of the `data` parameter.  

| Format | C Type       | Python Type       | Standard Size |
|--------|--------------|-------------------|---------------|
| `c`    | char         | bytes of length 1 | 1             |
| `s`    | char[]       | bytes             |               |
| `i`    | int          | integer           | 4             |
| `I`    | unsigned int | integer           | 4             |
The packet is then created by packing the header fields and the data using `struct.pack()`. The header fields are passed as arguments to struct.pack(), along with their corresponding format specifiers.

Finally, the `send_length()` function is called to send the packet length followed by the packet data.
```py
def send_length(sock, data):
    length = len(data)
    sock.send(struct.pack('!I', length))
    sock.send(data)
```
The `send_length()` function is responsible for sending the length of the packet before sending the actual packet data.  

The `recv_message()` function is responsible for receiving a packet from a socket connection. It takes the socket connection (`sock`) as a parameter.
The function first calls the `recv_length()` function, which receives the length of the next packet sent by the `send_length()` function. The received length is then passed to `sock.recv()` to receive the complete packet.
```py
def recv_length(sock):
    lengthbuf = sock.recv(4)
    length, = struct.unpack('!I', lengthbuf)
    return sock.recv(length)
```
```py
def recv_message(sock):
    data = recv_length(sock)

    #data = sock.recv(1024)
    message_length = int.from_bytes(data[8:13], byteorder='big', signed=False)
    
    hdr_fmt = f"c8si{message_length}s"
    return struct.unpack(hdr_fmt, data)
```
The length of the `Data` field of the packet is then retrieved from the packet and stored in the `message_length` variable in order to format the header (`hdr_fmt`) and unpack the struct. The unpacked values are returned.