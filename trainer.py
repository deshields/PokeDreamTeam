### For Enemy Trainer Single Battle
import csv
import pandas as pd
import pokebase as pb

from poke import PokemonMember

class TrainerAI(AI):

    def __init__(self, name, team, side, items, region):
        ### Gen = region
        assert(side == "ALLY" or side == "ENEMY")
        assert(team != [])
        assert(region == "KANTO" or region == "JOHTO" or region == "HOENN" or region == "SINNOH" or region == "UNOVA")
        self.name = name # String - optional
        self.team = team # List of strings [ ["pikachu", 10], ["lickitung", 15] ]
        self.team_count = len(team)
        self.poke_team = []
        makeTeam()
        self.lead = self.poke_team[0]
        self.lead_index = 0
        self.items = items # if use is true, list of strings, otherwise null
        self.region = region # String - optional


    def __repr__(self):

        print("Trainer: " + self.name)
        print("Leading Pokemon: " + self.team[0])
        print("Region: " + self.region)

    def makeTeam(self):
        for p in team:
            self.poke_team.append(PokemonMember(p[0], p[1]))

    def nextMove(self):
        if(self.items != [] and self.lead.cur_hp <= self.lead.hp * .15):
            # TODO: INITIALIZE ITEMS
            # use self.items[0]

        elif(self.team_count > 1 and (self.lead.cur_hp == self.lead.hp * .2 and self.lead.status != "NONE")):
            #When to switch


            self.lead_index += 1
            if(self.lead_index >= self.team_count):
                self.lead_index = 0

            while(self.poke_team[self.lead_index].cur_hp <= 0):
                self.lead_index += 1

            self.lead = self.poke_team[self.lead_index]

        else:
            print("Move")
