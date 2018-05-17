import csv
import pandas as pd
import pokebase as pb
from numpy import random
import math

df = pd.read_csv('pokemon.csv', index_col = 30) # Read by Pokemon Name

class PokemonMember:

    def __init__(self, name, lvl):
        self.name = name.title()
        self.level = lvl
        self.ability = df.loc[self.name]['abilities']
        self.hp = df.loc[self.name]['hp']
        self.att = df.loc[self.name]['attack']
        self.defe = df.loc[self.name]['defense']
        self.spatt = df.loc[self.name]['sp_attack']
        self.spdef = df.loc[self.name]['sp_defense']
        self.speed = df.loc[self.name]['speed']

        self.leading = False
        self.status = "NONE"

        self.calculateStats()

        self.cur_hp = self.hp

    def __repr__(self):
        print("Name: ", self.name)
        print("Level: ", self.level)
        print("HP: ", self.hp)
        print("Attack: ", self.att)
        print("Defense: ", self.defe)
        print("Sp. Attack: ", self.spatt)
        print("Sp. Defense: ", self.spdef)
        print("Speed: ", self.speed)

    def calculateStats(self):
        self.att = math.floor(math.floor((2 * self.att + 0 + random.randint(0, 63)) * self.level / 100 + 5) * 1)
        self.defe = math.floor(math.floor((2 * self.defe + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spatt = math.floor(math.floor((2 * self.spatt + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spdef = math.floor(math.floor((2 * self.spdef + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.speed = math.floor(math.floor((2 * self.speed + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.hp = math.floor((2 * self.speed + 0 + random.randint(0,63)) * self.level / 100) + 10 + self.level

    #Stat = math.floor(math.floor((2 * B + I + E) * L / 100 + 5) * N)
    # B - Base, I - Individual Value, E - Effort Value, L - Level, N - Nature (assume 1)

    #def moveSet(self):

print(PokemonMember('luxray', 40))
