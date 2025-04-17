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
message_receive =json.loads(message.decode())
if message_receive["response"] == "ok":
  s_serveur = socket.socket()
  s_serveur.bind(('0.0.0.0',port_perso))
  s_serveur.listen()
  client, address = s_serveur.accept()
  with client:
    message = client.recv(1024)
    print(message.decode())


#python3 server.py quarto
#python3 player.py