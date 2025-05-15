import socket
import json
import time
import copy
from collections import defaultdict

#variables initiales
port_perso = 6000
port_serveur_global = 3000 # connection au serveur du prof
IP_serveur_global = "localhost" 
name = "Vénéré_maîtresse"
matricules = ["23342", "23268"]

def timeit(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = fun(*args, **kwargs)
        print('Executed in {}s'.format(time.time() - start))
        return res
    return wrapper

def same(L):
    if None in L:
        return False
    common = set(L[0])
    for elem in L[1:]:
        common &= set(elem)
    return len(common) > 0

def getLine(board, i):
    return board[i * 4: (i + 1) * 4]

def getColumn(board, j):
    return [board[i] for i in range(j, 16, 4)]

def getDiagonal(board, dir):
    start = 0 if dir == 1 else 3
    return [board[start + i * (4 + dir)] for i in range(4)]

def isWinning(board):
    for i in range(4):
        if same(getLine(board, i)) or same(getColumn(board, i)):
            return True
    return same(getDiagonal(board, 1)) or same(getDiagonal(board, -1))

def isFull(board):
    return all(elem is not None for elem in board)

def gameOver(state):
    return isWinning(state['board']) or isFull(state['board'])

def moves(game_board, piece):
    all_pieces = [f"{s}{c}{w}{sh}" for s in "BS" for c in "DL" for w in "EF" for sh in "CP"]
    used_pieces = [p for p in game_board if p is not None]
    available_pieces = [p for p in all_pieces if p not in used_pieces and p != piece]
    positions = [i for i, val in enumerate(game_board) if val is None]
    result = {}
    nb = 0
    for pos in positions:
        for p in available_pieces:
            nb += 1
            result[nb] = {"pos": pos, "piece": p}
    return result

def apply(state, move):
    newState = copy.deepcopy(state)
    newState["board"][move["pos"]] = state["piece"]
    newState["piece"] = move["piece"]
    newState["current"] = (state["current"] + 1) % 2
    return newState

def fill_Lines(board):
    lines = [getDiagonal(board, 1), getDiagonal(board, -1)]
    for i in range(4):
        lines.append(getLine(board, i))
        lines.append(getColumn(board, i))
    return lines

def lineValue(line):
    if None in line:
        return 0
    common = set(line[0])
    for elem in line[1:]:
        common &= set(elem)
    return 1 if common else 0

def heuristic(state, player):
    if isWinning(state["board"]):
        return 9 if state["players"][state["current"]] == player else -9
    return sum(lineValue(line) for line in fill_Lines(state["board"]))

@timeit
def negamaxWithPruningIterativeDeepening(state, player, timeout=0.03):
	cache = defaultdict(lambda : 0)
	def cachedNegamaxWithPruningLimitedDepth(state, player, depth, alpha=float('-inf'), beta=float('inf')):
		over = gameOver(state)
		if over or depth == 0:
			res = -heuristic(state, player), None, over

		else:
			theValue, theMove, theOver = float('-inf'), None, True
			possibilities = [(move, apply(state, move)) for move in moves(state["board"],state['piece'] ).values()]
			possibilities.sort(key=lambda poss: cache[tuple(poss[1])])
			for move, successor in reversed(possibilities):
				value, _, over = cachedNegamaxWithPruningLimitedDepth(successor, state["current"]%2+1, depth-1, -beta, -alpha)
				theOver = theOver and over
				if value > theValue:
					theValue, theMove = value, move
				alpha = max(alpha, theValue)
				if alpha >= beta:
					break
			res = -theValue, theMove, theOver
		cache[tuple(state)] = res[0]
		return res

	value, move = 0, None
	depth = 1
	start = time.time()
	over = False
	while value > -9 and time.time() - start < timeout and not over:
		value, move, over = cachedNegamaxWithPruningLimitedDepth(state, player, depth)
		depth += 1

	return value, move

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
        _,move = negamaxWithPruningIterativeDeepening(message_receive_ping["state"],message_receive_ping["state"]["players"][message_receive_ping["state"]["current"]])
        move_sent = { "response": "move","move": move,"message": "Calcul terminé. Ton échec est inévitable. Prépare-toi à perdre."}
        client.sendall(json.dumps(move_sent).encode())

  # python3 server.py quarto
  # python3 player_ai_socket.py
  # python3 -m pip install -r requirements.txt