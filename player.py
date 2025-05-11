import socket
import json
import random

#variables initiales
port_perso = 6060
port_serveur_global = 3000 # connection au serveur du prof
IP_serveur_global = "localhost"  # "172.17.10.133" adress IP du serveur du prof # Il faut etre connecté au wifi PI2C
name = "Vénéré_maîtresse"
matricules = ["23300", "23200"]
chosen_pieces =[]
all_position = []


def generated_pieces(): # génèrer la liste de tous les moves
          chosen_pieces.clear()
          # Big/Small: B/S
          # Dark/Light: D/L
          # Empty/Full: E/F
          # Cylinder/Prism: C/P
          for size in ["B", "S"]:
              for color in ["D", "L"]:
                  for weight in ["E", "F"]:
                      for shape in ["C", "P"]:
                          chosen_pieces.append(f"{size}{color}{weight}{shape}")


def input_move(game_board,piece): #choisit les move de manière random
              generated_pieces()
              # Move
          # {
          #   "pos": <index>,        # between 0 and 15 or null if first move
          #   "piece": <piece_str>,  # piece for the opponent example "BDEC"
          # }
              all_position =list(range(len(game_board))) #range renvoie une object range donc il faut transformer en liste
               #permte de connaitre l'indice d'un object sur le plateau de jeux 
              for index, n in enumerate(game_board):
                  if n != None:
                      if n in chosen_pieces:
                        chosen_pieces.remove(n)
                      if index in all_position: 
                          all_position.remove(index)
              pos = random.choice(all_position)
              if piece!= None :  #pour éviter les bad moves causé par la piece choisit par notre adversaire
                if piece in chosen_pieces:
                    chosen_pieces.remove(piece)
              piece = random.choice(chosen_pieces)
              if len(piece) == 0:
                  piece = None
              return {"pos": pos, "piece": piece}




if __name__ == "__main__":
  socket_inscription = socket.socket() #TCP
  socket_inscription.connect((IP_serveur_global,port_serveur_global))
  socket_serveur_local = socket.socket()
  socket_serveur_local.bind(('0.0.0.0',port_perso))
  #Inscription au serveur
  message_connection = {
    "request": "subscribe",
    "port": port_perso,
    "name": name,
    "matricules": matricules
  }
  socket_inscription.send(json.dumps(message_connection).encode()) #!!!!!! json.dumps().encode(), il faut pas oublié encode()
  message = socket_inscription.recv(1024)
  message_receive =json.loads(message.decode())


  #Communication serveur (envoyer et recevoir information)
  while message_receive["response"] == "ok":
    socket_serveur_local.listen()
    client, address = socket_serveur_local.accept() #client : la méthode accept(), Renvoie un tuple avec un socket client et l’adresse de ce dernier, ce socket client est celui qui doit être utiliser pour communiquer (envoyer et recevoir info) car il reste constament connecter au client donc pas de [Errno 32] Broken pipe
    with client:
      message_ping = client.recv(1024)
      message_receive_ping =json.loads(message_ping.decode())
      if message_receive_ping["request"] == "ping":
        message_pong = {"response": "pong"}
        client.sendall(json.dumps(message_pong).encode())
      elif message_receive_ping["request"] == "play": 
        move = input_move(message_receive_ping["state"]["board"],message_receive_ping["state"]["piece"])
        move_sent = { "response": "move","move": move,"message": "Fun message"}
        client.sendall(json.dumps(move_sent).encode())

  # python3 server.py quarto
  # python3 player.py
  # python3 -m pip install -r requirements.txt