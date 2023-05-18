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