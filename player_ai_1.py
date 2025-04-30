# The game state is state = {"players": players, "current": 0, "board": [None] * 16, "piece": None}
# None is stored for empty cell
# 0 is stored for 'LUR' (player 1)
# 1 is stored for 'FKY' (player 2)
import random
import copy
import time

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

def gameOver(state):
	if isWinning(state) is not None:
		return True
     
def isFull(board):
    for elem in board:
        if elem is None:
            return False
    return True


def Quarto(players):
    if len(players) != 2:
        raise ValueError("Tic Tac Toe must be played by 2 players")

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
    @timeit
    def next(state, move):
        newState = copy.deepcopy(state)

        if state["piece"] is not None:
            if "pos" not in move:
                raise ValueError("Move must contains a 'pos' key")

            try:
                pos = int(move["pos"])
                state["board"][pos]
            except (ValueError, IndexError):
                raise ValueError(
                    "Move['pos'] must be an integer between 0 and 15 inclusive"
                )

            if state["board"][pos] is not None:
                raise ValueError(f"These place '{pos}' is not free")

            newState["board"][pos] = state["piece"]

            if isWinning(newState["board"]):
                #print(f"{state["current"]}: win the game")
                raise TimeoutError

            if isFull(newState["board"]):
                print (newState,"Draw")

        if "piece" not in move:
            raise ValueError("Move must contains a 'piece' key")

        if not isinstance(move["piece"], str):
            raise ValueError("Move['piece'] must be a str")

        piece = frozenset(move["piece"])

        if piece not in pieces:
            print(pieces)
            raise ValueError(f"Piece '{move['piece']}' not available")

        newState["piece"] = move["piece"]

        newState["current"] = (state["current"] + 1) % 2
        pieces.remove(piece)
        return newState

    return state, next

chosen_pieces =[]
all_position = []
lines =[]

def show(board):
    for i in range(4):
        print(getLine(board, i))

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
              generated_pieces() # à chaque fois qu'on fait un move, on suprime l'ancienne liste et on génère une nouvelle
              # Move
          # {
          #   "pos": <index>,        # between 0 and 15 or null if first move
          #   "piece": <piece_str>,  # piece for the opponent example "BDEC"
          # }
              all_position =list(range(len(game_board))) #range renvoie une object range donc il faut transformer en liste
              index = 0 #permte de connaitre l'indice d'un object sur le plateau de jeux 
              for n in game_board:
                  if n != None:
                      if n in chosen_pieces:
                        chosen_pieces.remove(n)
                      if index in all_position: 
                          all_position.remove(index)
                  index +=1
              pos = random.choice(all_position)
              if piece!= None :  #pour éviter les bad moves causé par la piece choisit par notre adversaire
                if piece in chosen_pieces:
                    chosen_pieces.remove(piece)
              piece = random.choice(chosen_pieces)
              if len(piece) == 0:
                  piece = None
              return {"pos": pos, "piece": piece}

def timeit(fun):
	def wrapper(*args, **kwargs):
		start = time.time()
		res = fun(*args, **kwargs)
		print('Executed in {}s'.format(time.time() - start))
		return res
	return wrapper

state, next = Quarto(["LUR", "FKY"])
try:
    while True:
        show(state["board"])
        print(f"Piece: {state['piece']}")
        print(f"Player: {state['players'][state['current']]}") # attention avec f"...''..."
        move = input_move(state["board"],[state["piece"]])
        try:
                state = next(state, move)
        except ValueError as e:
                print(e)
except TimeoutError:
        show(state["board"])
        print("{} win the game".format(state["players"][state["current"]]))
