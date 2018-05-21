### For Enemy Trainer Single Battle
import csv
import pandas as pd
import pokebase as pb

from poke import PokemonMember

def set_opponent(TrainerA, TrainerB):
    TrainerA.opponent.append(TrainerB)
    TrainerB.opponent.append(TrainerA)


class TrainerAI(AI):

    def __init__(self, name, team, side, items, region):
        ### Gen = region
        assert(side == "ALLY" or side == "ENEMY")
        assert(team != [])
        assert(region == "KANTO" or region == "JOHTO" or region == "HOENN" or region == "SINNOH" or region == "UNOVA")
        self.name = name # String - optional
        self.team = team # List of strings [ ["pikachu", 10, ["thunderbolt", "spark"]], ["lickitung", 15, ["confuse ray", "lick"]] ]
        self.team_count = len(team)
        self.poke_team = []
        makeTeam()
        self.lead = self.poke_team[0]
        self.lead_index = 0
        self.items = items # if use is true, list of strings, otherwise null
        self.region = region # String - optional
        self.opponent = []


    def __repr__(self):

        print("Trainer: " + self.name)
        print("Leading Pokemon: " + self.team[0])
        print("Region: " + self.region)

    def makeTeam(self):
        """ Converts string team input to PokemonMember class """
        for p in team:
            self.poke_team.append(PokemonMember(p[0], p[1], p[2]))

    def findEff(self):
        """ Finds the effectiveness of the user's leading pokemon's moveset against the type of the opponent. """
        move_eff = []
        for i in range(len(self.moveData)):
            move_eff.append(self.lead.checkEffectiveness(i, self.opponent[0].lead.type))
        return move_eff


    def nextTurn(self):
        """ Trainer decides what the next best move should be """


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

            print("Switched out " + self.lead + " for " + self.poke_team[self.lead_index])
            self.lead = self.poke_team[self.lead_index]


        else:
            # TODO: Do we want to inflict damgage, increase/decrease stats, or inflict a status move?
            # If status, does the opponent already have a status issue?
            # If no, go for it. If sleep, frozen, or paralyze, increase your stats and attack next turn.
            # Check if the move inflicts damage or is a status move.

            # TODO: Do pre-calculations as to possible damage outcomes then choose the highest for next damaging move
            check = max(findEff())
