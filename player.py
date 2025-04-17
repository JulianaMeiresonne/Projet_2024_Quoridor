import socket
import threading
import time
import json

port_perso = 8888
port_serveur_prof = 3000
Ip_prof = "localhost"

s = socket.socket() #TCP
s.connect(('localhost',port_serveur_prof))
message_connection = {
  "request": "subscribe",
  "port": 8888,
  "name": "fun_name_for_the_client",
  "matricules": ["12345", "67890"]
}
s.send(json.dumps(message_connection).encode()) #!!!!!! json.dumps().encode(), il faut pas oublié encode()
message = s.recv(1024)
print(message.decode())