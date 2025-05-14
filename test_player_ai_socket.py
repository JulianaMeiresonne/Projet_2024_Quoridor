import pytest
import player_ai_socket

state={"board": {                                                          #on définit un plateau avec certaine pièce placée
            (0, 0): "BDEC",(0, 1): None,(0,2):None,(0,3):None,
            (1, 1): None, (1, 1): None,(1,2):None,(1,3):None,
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

def test_moves():
    # Définir un plateau de jeu avec certaines pièces placées
    game_board={(0, 0): "BDEC",(0, 1): None,(0,2):None,(0,3):None,
            (1, 1): None, (1, 1): None,(1,2):None,(1,3):None,
            (2, 0): "BDEP",(2, 1): None,(2,2):None,(2,3):None,
            (3, 0): "BLEC",(3, 1): None,(3,2):None,(3,3):None
                }
    piece = "BSCP"  # La pièce que vous souhaitez tester
    result = player_ai_socket.moves(game_board, piece)
    for move in result.values():
        assert move["piece"] != piece


 

