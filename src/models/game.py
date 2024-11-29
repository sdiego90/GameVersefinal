# src/models/game.py
class Game:
    def __init__(self, name, price, genre, esrb, stock, platform):
        self.name = name
        self.price = price
        self.genre = genre
        self.esrb = esrb
        self.stock = stock
        self.platform = platform