# Lab Assignment-1 
### Design of an end to end messaging system like WhatsApp
- The application supports peer to peer communication with one server component and multiple client components.
- Messages and files exchanged between peers are encrypted using `3DES` algorithm. Key exchange is done using `Diffie Hellman Key Exchange` algorithm.
- Messages and files sent to groups are encrypted using `3DES` algorithm.
- The application is built using Object Oriented Programming (OOPs) paradigms.
### Steps to run:
- To run server : `python3 server.py`
- To run client : `python3 client.py <portno.>`
### Commands used:
- `signup <userid> <password>`
Usernames are assumed to be unique. Appropriate message is printed if same username is given more than once.
- `login <userid> <password>`
Appropriate message is displayed if the user has already logged in.
- `list`
Each user can use this command to list the group name and number of members in each group respectively.
- `create <groupid>`
Any user can create a group with given groupname. The user creating the group is added to it by default.
- `join <groupid>`
To join a group. If no such group exists, a new group is created and the user is added to it.
- `send <userid> <msg>`
To send a msg to the given user.
- `send file <filepath> <userid>`
To send a file to the given user.
- `send file <filepath> <groupid>`
To send a file to every member of the group.
- `send <groupid> <msg>`
To send a msg to every member of the group.