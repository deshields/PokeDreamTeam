import csv
import pandas as pd
import pokebase as pb
from numpy import random
import math

df = pd.read_csv('pokemon.csv', index_col = 30) # Read by Pokemon Name
tc = pd.read_csv('type_chart.csv', index_col = 0)

class PokemonMember:

    def __init__(self, name, abil, lvl, moves, item):
        # TODO: account for hidden ability?

        self.name = name.title()
        self.level = lvl
        self.type = [df.loc[self.name]['type1']]
        if df.loc[self.name]['type2'] != "" and type(df.loc[self.name]['type2']) is not float:
            self.type.append(df.loc[self.name]['type2'])

        self.ability = abil if abil != [] else df.loc[self.name]['abilities']
        self.hp = df.loc[self.name]['hp']
        self.att = df.loc[self.name]['attack']
        self.defe = df.loc[self.name]['defense']
        self.spatt = df.loc[self.name]['sp_attack']
        self.spdef = df.loc[self.name]['sp_defense']
        self.speed = df.loc[self.name]['speed']

        self.apiData = pb.pokemon(name.lower())

        self.moves = moves #A list of strings
        self.moveData = [''] * len(moves) # move objects from API
        self.pp = [0] * len(moves)
        self.held_item = item # string until item class is made

        self.status = ["NONE", -1] # "FAINTED", "SLEEP", "PARALYZED", "FROZEN", "BADLY POISONED", "POISONED", "BURNED" - if [-1] is the second value, then it stays until cured
        self.sub_status = [] # "INLOVE", "CONFUSED", "PROTECTED", "AIRBORNE", "LOCKED ON" <- Basically the stackable statuses
        self.canBattle = True #False means "Fainted"
        self.pokeScore = 0


        # TODO: IMPLEMENT HELD ITEMS

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
        print("Held Item: ", self.held_item)
        return ""

    def calculateStats(self):
        """ Using the stat formula, calculate stats. IV is omitted from calculation and assume a random Effort value """

        self.att = math.floor(math.floor((2 * self.att + 0 + random.randint(0, 63)) * self.level / 100 + 5) * 1)
        self.defe = math.floor(math.floor((2 * self.defe + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spatt = math.floor(math.floor((2 * self.spatt + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.spdef = math.floor(math.floor((2 * self.spdef + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.speed = math.floor(math.floor((2 * self.speed + 0 + random.randint(0 ,63)) * self.level / 100 + 5) * 1)
        self.hp = math.floor((2 * self.speed + 0 + random.randint(0,63)) * self.level / 100) + 10 + self.level

    def getMoveData(self):

        """ Convert the string input to move data using the pokebase api """

        for i in range(len(self.moves)):
            name = self.moves[i].replace(" ", "-")
            self.moveData[i] = pb.move(name)
            self.pp[i] = self.moveData[i].pp

    def checkEffectiveness(self, move_index, opp_type):

        """ Checks effectiveness of a move against the opponent's type """

        e = 1
        for t in opp_type:
            tt = t.title()
            move = self.moveData[move_index].type.name.title()
            e = e * tc.loc[move][tt]
        return e

#print(PokemonMember('luxray', [], 40, ["spark", "bite", "charge", "quick attack"], "NONE"))
