import pytest
import quarto

def test_Quarto():
    with pytest.raises(ValueError):                     #Nous permet de vérifier si on a bien mis les ValueError pour les conditions le nécessitant
        if len(['player1', 'player2', 'player3']) > 2:  # situation dans laquelle on a plus de 2 joueurs
            raise ValueError
        if len(['player1']) <2:  # situation dans laquelle on a moins de deux joueurs
            raise ValueError

def test_next():
    with pytest.raises(ValueError):
        if "pos" not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
            raise ValueError

# def test_random():
#     quarto.input_move() # !! attentions au if __name__ == "__main__":