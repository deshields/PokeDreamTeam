from trainer import *
from player import *

class Battle:
    # Single Battle Only For Now, not taking player items into account
    def __init__(self, battle_type, players):
        assert(battle_type == 'SINGLE' or battle_type == 'DOUBLE')
        self.battle_type = battle_type
        self.players = players #list of trainer classes
        round = 0
        weather = "clear"

    def round():
        round += 1
