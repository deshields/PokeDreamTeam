import csv
import pandas as pd
import pokebase as pb
from numpy import random
import math

df = pd.read_csv('pokemon.csv', index_col = 30) # Read by Pokemon Name

class PokemonMember:

    def __init__(self, name, lvl, moves):
        self.name = name.title()
        self.level = lvl
        self.type = [df.loc[self.name]['type1']]
        if df.loc[self.name]['type2'] != "":
            self.type.append(df.loc[self.name]['type2'])
        self.ability = df.loc[self.name]['abilities']
        self.hp = df.loc[self.name]['hp']
        self.att = df.loc[self.name]['attack']
        self.defe = df.loc[self.name]['defense']
        self.spatt = df.loc[self.name]['sp_attack']
        self.spdef = df.loc[self.name]['sp_defense']
        self.speed = df.loc[self.name]['speed']

        self.moves = moves #A list of strings
        self.moveData = [''] * len(moves)

        self.leading = False
        self.status = "NONE"

        self.calculateStats()
        self.getMoveData()

        self.cur_hp = self.hp

    def __repr__(self):
        print("Name: ", self.name)
        print("Type: ", self.type)
        print("Level: ", self.level)
        print("HP: ", self.hp)
        print("Attack: ", self.att)
        print("Defense: ", self.defe)
        print("Sp. Attack: ", self.spatt)
        print("Sp. Defense: ", self.spdef)
        print("Speed: ", self.speed)
        print("Moves ", self.moves)

    def calculateStats(self):
        self.att = math.floor(math.floor((2 * self.att + 0 + random.randint(0, 63)) * self.level / 100 + 5) * 1)
        self.defe = math.floor(math.floor((2 * self.defe + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spatt = math.floor(math.floor((2 * self.spatt + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spdef = math.floor(math.floor((2 * self.spdef + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.speed = math.floor(math.floor((2 * self.speed + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.hp = math.floor((2 * self.speed + 0 + random.randint(0,63)) * self.level / 100) + 10 + self.level

    #Stat = math.floor(math.floor((2 * B + I + E) * L / 100 + 5) * N)
    # B - Base, I - Individual Value, E - Effort Value, L - Level, N - Nature (assume 1)

    def getMoveData(self):
        for i in range(len(self.moves)):
            name = self.moves[i].replace(" ", "-")
            #print(self.moves[i])
            self.moveData[i] = pb.move(name)

    def checkEffectiveness(self, move_index, opp_type):
        e = 1
        for t in opp_type:
            check = "against_" + self.moveData[i].type
            e = e * df.loc[self.name][check]
        return e

print(PokemonMember('luxray', 40, ["spark", "bite", "charge", "quick attack"]))
