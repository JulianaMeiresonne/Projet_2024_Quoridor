import pytest
import quarto

def test_Quarto():
    with pytest.raises(ValueError):                     #Nous permet de vérifier si on a bien mis les ValueError pour les conditions le nécessitant
        if len(['player1', 'player2', 'player3']) > 2:  # situation dans laquelle on a plus de 2 joueurs
            raise ValueError
        if len(['player1']) <2:  # situation dans laquelle on a moins de deux joueurs
            raise ValueError
state={"board": {                                                          #on définit un plateau avec certaine pièce placée
            (0, 0): "piece1",(0, 1): None,(0,2):None,(0,3):None,
            (1, 1): None, (1, 1): None,(1,2):None,(1,3):None,
            (2, 0): "piece2",(2, 1): None,(2,2):None,(2,3):None,
            (3, 0): "piece3",(3, 1): None,(3,2):None,(3,3):None,
            }
        }
pos=(0,0)                                                                   #on prends une position ayant déjà une pièce pour tester l'erreur
def test_next():
    with pytest.raises(ValueError):
        if "pos" not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
            raise ValueError
        if state["board"][pos] is not None:
            raise ValueError

# def test_random():
#     quarto.input_move() # !! attentions au if __name__ == "__main__":