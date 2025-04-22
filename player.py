import socket
import json

port_perso = 8888
port_serveur_global = 3000 # connection au serveur du prof
IP_serveur_global = "172.17.10.133" # adress IP du serveur du prof

#Inscription au serveur
s_inscription = socket.socket() #TCP
s_inscription.connect((IP_serveur_global,port_serveur_global))
message_connection = {
  "request": "subscribe",
  "port": port_perso,
  "name": "Vénéré_maîtresse",
  "matricules": ["23342", "23268"]
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
      if __name__ == "__main__":
        import os
        import sys

        sys.path.append(os.getcwd())

      import copy
      import random


      def same(L):
        if None in L:
          return False
        common = frozenset(L[0])
        for elem in L[1:]:
          common = common & frozenset(elem)
        return len(common) > 0


      def getLine(board, i):
          return board[i * 4 : (i + 1) * 4]


      def getColumn(board, j):
          return [board[i] for i in range(j, 16, 4)]


      # dir == 1 or -1
      def getDiagonal(board, dir):
          start = 0 if dir == 1 else 2
          return [board[start + i * (4 + dir)] for i in range(4)]


      def isWinning(board):
          for i in range(4):
              if same(getLine(board, i)):
                  return True
              if same(getColumn(board, i)):
                  return True
          if same(getDiagonal(board, 1)):
              return True
          return same(getDiagonal(board, -1))


      def isFull(board):
          for elem in board:
              if elem is None:
                  return False
          return True


      def Quarto(players):
          if len(players) != 2:
              print("Tic Tac Toe must be played by 2 players")
              raise ValueError
          #game.BadGameInit("Tic Tac Toe must be played by 2 players")

          # Big/Small: B/S
          # Dark/Light: D/L
          # Empty/Full: E/F
          # Cylinder/Prism: C/P
          pieces = set()
          for size in ["B", "S"]:
              for color in ["D", "L"]:
                  for weight in ["E", "F"]:
                      for shape in ["C", "P"]:
                          pieces.add(frozenset({size, color, weight, shape}))

          state = {"players": players, "current": 0, "board": [None] * 16, "piece": None}

          # Move
          # {
          #   "pos": <index>,        # between 0 and 15 or null if first move
          #   "piece": <piece_str>,  # piece for the opponent example "BDEC"
          # }

          def next(state, move):
              newState = copy.deepcopy(state)

              if state["piece"] is not None:
                  if "pos" not in move:
                      print("Move must contains a 'pos' key")
                      raise ValueError
                  #game.BadMove("Move must contains a 'pos' key")

                  try:
                      pos = int(move["pos"])
                      state["board"][pos]
                  except (ValueError, IndexError):
                      print("Move['pos'] must be an integer between 0 and 15 inclusive")
                      raise ValueError
                  #game.BadMove("Move['pos'] must be an integer between 0 and 15 inclusive")

                  if state["board"][pos] is not None:
                      print(f"These place '{pos}' is not free")
                      raise ValueError
                  #game.BadMove(f"These place '{pos}' is not free")

                  newState["board"][pos] = state["piece"]

                  if isWinning(newState["board"]):
                      print(state["current"], newState)
                      raise ValueError
                  #game.GameWin(state["current"], newState)

                  if isFull(newState["board"]):
                      print(newState)
                      raise ValueError
                  # game.GameDraw(newState)

              if "piece" not in move:
                  print("Move must contains a 'piece' key")
                  raise ValueError
              # game.BadMove("Move must contains a 'piece' key")

              if not isinstance(move["piece"], str):
                  print("Move['piece'] must be a str")
                  raise ValueError
              #game.BadMove("Move['piece'] must be a str")

              piece = frozenset(move["piece"])

              if piece not in pieces:
                  print(pieces)
                  print(f"Piece '{move['piece']}' not available")
                  raise ValueError
              # game.BadMove(f"Piece '{move['piece']}' not available")

              newState["piece"] = move["piece"]

              newState["current"] = (state["current"] + 1) % 2
              pieces.remove(piece)
              return newState

          return state, next


      Game = Quarto

      if __name__ == "__main__":

          def show(board):
              for i in range(4):
                  print(getLine(board, i))

          def input_move(player):
              print(f"player {player}")
              #pos = input("Pos (enter for `null`): ")
              pos = random.choice("0,1,2,3,4,5,6,7,8,9,10,11,12,13,14")
              if len(pos) == 0:
                  pos = None
              else:
                  pos = int(pos)
              piece = random.choice(['BLEP','SLFC','BDEC','BLFP','BLEC'])
              if len(piece) == 0:
                  piece = None
              return {"pos": pos, "piece": piece}

          state, next = Quarto([message_receive_ping["state"]["players"][0],message_receive_ping["state"]["players"][1]])
          try:
              while True:
                  show(state["board"])
                  print(f"Piece: {state['piece']}")
                  move = input_move(state["players"][state["current"]])
                  move_sent = {
                                "response": "move",
                                "move": move,
                                "message": "Fun message"
                              }
                  client.send(json.dumps(move_sent).encode())
                  try:
                      state = next(state, move)
                  except ValueError as e:
                      print(e)
          except ValueError as e:
            #   show(e.state["board"])
            #   print("{} win the game".format(state["players"][e.winner]))
              print("game over")

# python3 server.py quarto
# python3 player.py