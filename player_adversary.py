import socket
import json
import copy
import random
port_perso = 6000
port_serveur_global = 3000 # connection au serveur du prof
IP_serveur_global = "localhost" # adress IP du serveur du prof, 172.17.10.133.3000 avec 3000 = port donc il faut pas le mettre car déja mit

#Inscription au serveur
s_inscription = socket.socket() #TCP
s_inscription.connect((IP_serveur_global,port_serveur_global))
message_connection = {
  "request": "subscribe",
  "port": port_perso,
  "name": "player_adversary",
  "matricules": ["23000", "23001"]
}
s_inscription.send(json.dumps(message_connection).encode()) #!!!!!! json.dumps().encode(), il faut pas oublié encode()
message = s_inscription.recv(1024)
message_receive =json.loads(message.decode())
print(message)


#Communication serveur (envoyer et recevoir information)
s_serveur = socket.socket()
s_serveur.bind(('0.0.0.0',port_perso))
while message_receive["response"] == "ok":
  s_serveur.listen()
  client, address = s_serveur.accept() #client : la méthode accept(), Renvoie un tuple avec un socket client et l’adresse de ce dernier, ce socket client est celui qui doit être utiliser pour communiquer (envoyer et recevoir info) car il reste constament connecter au client donc pas de [Errno 32] Broken pipe
  with client:
    message_ping = client.recv(1024)
    message_receive_ping =json.loads(message_ping.decode())
    if message_receive_ping["request"] == "ping":
      message_pong = {"response": "pong"}
      client.send(json.dumps(message_pong).encode())
    elif message_receive_ping["request"] == "play":
      chosen_pieces =[]
      def generated_pieces():
          # Big/Small: B/S
          # Dark/Light: D/L
          # Empty/Full: E/F
          # Cylinder/Prism: C/P
          for size in ["B", "S"]:
              for color in ["D", "L"]:
                  for weight in ["E", "F"]:
                      for shape in ["C", "P"]:
                          chosen_pieces.append(f"{size}{color}{weight}{shape}") # generer la liste de tous les moves

          # Move
          # {
          #   "pos": <index>,        # between 0 and 15 or null if first move
          #   "piece": <piece_str>,  # piece for the opponent example "BDEC"
          # }
      def input_move():
              pos = random.choice([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
              piece = random.choice(chosen_pieces)
              if len(piece) == 0:
                  piece = None
              return {"pos": pos, "piece": piece}
      
      generated_pieces()
      move = input_move()
      move_sent = {
                                "response": "move",
                                "move": move,
                                "message": "Fun message"
                              }
      client.send(json.dumps(move_sent).encode())

# python3 server.py quarto
# python3 player_adversary.py