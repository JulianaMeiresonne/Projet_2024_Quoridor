import pytest
import player_ai_socket

state={"board": {                                                          #on définit un plateau avec certaine pièce placée
            (0, 0): "BDEC",(0, 1): None,(0,2):None,(0,3):None,
            (1, 0): None, (1, 1): None,(1,2):None,(1,3):None,
            (2, 0): "BDEP",(2, 1): None,(2,2):None,(2,3):None,
            (3, 0): "BLEC",(3, 1): None,(3,2):None,(3,3):None,
            }
        }
pos=(0,0)                                                                   #on prends une position ayant déjà une pièce pour tester l'erreur

def test_position():
    with pytest.raises(ValueError):
        if "pos" not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
            raise ValueError
        if state["board"][pos] is not None:
            raise ValueError

def test_same():
    assert player_ai_socket.same([[2, 2, 2], [2, 3, 4], [2, 5, 6]]) == True
    assert player_ai_socket.same([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == False

def test_getLine():
    # Cas de base : plateau standard
    board = ["BDEC", "BDEP", "BLEC", "BSCP",
            "SDEC", "SDEP", "SLEC", "SSCP",
            "BCEF", "BCEP", "BLEF", "BSCP",
            "SCEF", "SCEP", "SLEF", "SSCP" ]
    # Test de chaque ligne
    assert player_ai_socket.getLine(board, 0) == ["BDEC", "BDEP", "BLEC", "BSCP"]
    assert player_ai_socket.getLine(board, 1) == ["SDEC", "SDEP", "SLEC", "SSCP"]
    assert player_ai_socket.getLine(board, 2) == ["BCEF", "BCEP", "BLEF", "BSCP"]
    assert player_ai_socket.getLine(board, 3) == ["SCEF", "SCEP", "SLEF", "SSCP"]

def test_getColumn():
    board = ["BDEC", "BDEP", "BLEC", "BSCP",
            "SDEC", "SDEP", "SLEC", "SSCP",
            "BCEF", "BCEP", "BLEF", "BSCP",
            "SCEF", "SCEP", "SLEF", "SSCP" ]
    assert player_ai_socket.getColumn(board, 0) ==["BDEC","SDEC","BCEF","SCEF"]
    assert player_ai_socket.getColumn(board, 1) ==["BDEP","SDEP","BCEP","SCEP"]
    assert player_ai_socket.getColumn(board, 2) ==["BLEC","SLEC","BLEF","SLEF"]
    assert player_ai_socket.getColumn(board, 3) ==["BSCP","SSCP","BSCP","SSCP"]

def test_isWinning():
        board1=["BDEC","BDEP","BLEC","BSCP",None,None,None,None,None,None,None,None,None,None,None,None]
        board2=["BDEC",None,None,None,"BDEP",None,None,None,"BLEC",None,None,None,"BSCP",None,None,None]
        board3=["BDEC",None,None,None,None,"BDEP",None,None,None,None,"BLEC",None,None,None,None,"BSCP"]
        player_ai_socket.isWinning(board1)==True
        player_ai_socket.isWinning(board2)==True
        player_ai_socket.isWinning(board3)==True

def test_isFull():
        board=["BDEC", "BDEP", "BLEC", "BSCP","SDEC", "SDEP", "SLEC", "SSCP","BCEF", "BCEP", "BLEF", "BSCP","SCEF", "SCEP", "SLEF", "SSCP"]
        assert player_ai_socket.isFull(board)==True

def test_gameOver():
        state={"board":["BDEC","BDEP","BLEC","BSCP",None,None,None,None,None,None,None,None,None,None,None,None]}
        state_1={"board":["BDEC",None,None,None,"BDEP",None,None,None,"BLEC",None,None,None,"BSCP",None,None,None]}
        state_2={"board":["BDEC",None,None,None,None,"BDEP",None,None,None,None,"BLEC",None,None,None,None,"BSCP"]}
        state_3 = {"board": ["BDEC", "BDEP", "BLEC", "BSCP","SDEC", "SDEP", "SLEC", "SSCP","BCEF", "BCEP", "BLEF", "BSCP","SCEF", "SCEP", "SLEF", "SSCP"]}
        assert player_ai_socket.gameOver(state) == True
        assert player_ai_socket.gameOver(state_1) == True
        assert player_ai_socket.gameOver(state_2) == True
        assert player_ai_socket.gameOver(state_3) == True

def test_moves():
    game_board_1={(0, 0): "BDEC",(0, 1): None,(0,2):None,(0,3):None,
                (1, 0): None, (1, 1): None,(1,2):None,(1,3):None,
                (2, 0): "BDEP",(2, 1): None,(2,2):None,(2,3):None,
                (3, 0): "BLEC",(3, 1): None,(3,2):None,(3,3):None
                }
    game_board_2=["BDEC", "BDEP", "BLEC", "BSCP","SDEC", "SDEP", "SLEC", "SSCP","BCEF", "BCEP", "BLEF", "BSCP","SCEF", "SCEP", "SLEF", "SSCP"]

    piece = "BSCP"
    result_1 = player_ai_socket.moves(game_board_1, piece)
    result_2 = player_ai_socket.moves(game_board_1, piece)
    used_pieces = [p for p in game_board_1 if p is not None]
    for move in result_1.values():
        assert move["piece"] != piece
        assert piece not in used_pieces
    for move in result_2.values():
         assert len(result_2)==0

def test_apply():
    state={
          "board":[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
          "piece":"BDEC",
          "current": 0
     }
    move={
         "pos":0,
         "piece":"BSCP"
    }
    result = player_ai_socket.apply(state, move)
    assert result["board"][0]=="BDEC"
    assert result["piece"]=="BSCP"
    assert result["current"]==1

# coverage run -m pytest test_player_ai_socket.py 
# coverage report -m
