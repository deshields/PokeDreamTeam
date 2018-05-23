### For Enemy Trainer Single Battle
import csv
import pandas as pd
import pokebase as pb
from numpy import random

from poke import PokemonMember
#from battle import * # causes it to print twice

def set_opponent(TrainerA, TrainerB):
    TrainerA.opponent.append(TrainerB)
    TrainerB.opponent.append(TrainerA)

def makeAPIFriendly(l_string):
    """ Makes it easier for API to read
        l_string = list of strings """

    for i in range(len(l_string)):
        l_string[i] = l_string[i].replace(" ", "-")
        l_string[i] = l_string.lower()

    return l_string



class TrainerAI:

    def __init__(self, name, team, side, items, generation):

        assert(side == "A" or side == "B")
        assert(team != [])
        #assert(region == "KANTO" or region == "JOHTO" or region == "HOENN" or region == "SINNOH" or region == "UNOVA")
        self.name = name # String - optional
        self.team = team # List of strings [ ["pikachu", "", 10, ["thunderbolt", "spark"], ""], ["squirtle", "", 15, ["confuse ray", "lick"], ""] ]
        self.team_count = len(team)
        self.poke_team = []
        self.makeTeam()
        self.lead = self.poke_team[0]
        self.lead_index = 0
        self.items = items # if use is true, list of strings, otherwise null
        self.gen = generation # String - optional
        self.opponent = []

        self.prev_decision = ["None", "None"] # will update to ["Move", "Flamethrower"], ["Item", "Potion"], ["Switch", "Pokemon-Swapped-In"]


    def __repr__(self):

        print("Trainer: " + self.name)
        print("Leading Pokemon: " + self.lead.name)
        print("Current Health: " + str(self.lead.cur_hp) + " / " + str(self.lead.hp))
        print("Gen: " + str(self.gen))
        return ""

    def makeTeam(self):
        """ Converts string team input to PokemonMember class """
        for p in self.team:
            self.poke_team.append(PokemonMember(p[0], p[1], p[2], p[3], p[4]))

    def findEff(self):
        """ Finds the effectiveness of the user's leading pokemon's moveset against the type of the opponent. """
        move_eff = []
        for i in range(len(self.moveData)):
            move_eff.append(self.lead.checkEffectiveness(i, self.opponent[0].lead.type))
        return move_eff


    def DamageCalc(self, mi, battle):
        """ https://bulbapedia.bulbagarden.net/wiki/Damage , mi is the move index, battle is the battle class it's in"""

        if self.lead.moveset[mi].damage_type.name == 'physical':
            dmg = ( ( ( ( (2 * self.lead.level)/5 ) + 2 ) * self.lead.moveset[mi].power * (self.lead.att / self.opponent[0].lead.defe) ) / 50 ) + 2
            burn = 0.5 if self.lead.status == "BURN" else 1

        else:
            dmg = ( ( ( ( (2 * self.lead.level)/5 ) + 2 ) * self.lead.moveset[mi].power * (self.lead.spatt / self.opponent[0].lead.spdef) ) / 50 ) + 2
            burn = 1
        ### Modifier Calculations

        # Weather
        if (self.lead.moveset[mi].type.name == 'fire' and battle.weather == "SUNNY") or (self.lead.moveset[mi].type.name == 'water' and battle.weather == "RAIN"):
            w = 1.5
        elif (self.lead.moveset[mi].type.name == 'water' and battle.weather == "SUNNY") or (self.lead.moveset[mi].type.name == 'fire' and battle.weather == "RAIN"):
            w = 0.5

        else:
            w = 1

        # Random
        if self.gen > 2:
            r = random.uniform(0.85, 1.0)

            # BADGE GOES HERE

        else:
            r = random.randint(217,256)/255

        # STAB

        stab = 1.5 if self.lead.moveset[mi].type.name in self.lead.type else 1

        # Type effectiveness

        t = findEff()
        t = t[mi]

        # THIS MODIFIER IS ONLY TO BE USED FOR SINGLE BATTLES SINCE THERE IS ONE TARGET

        modifer = w * isCrit(mi) * r * stab * t * burn # * other ( * badge for gen ii)

        return modifier * dmg



    def isCrit(self, mi):
        """ Returns 2 if crit, if not return 1 """

        high_crit = ["10,000,000 Volt Thunderbolt", "Aeroblast", "Air Cutter", "Attack Order", "Blaze Kick", "Crabhammer", "Cross Chop", "Cross Poison", "Drill Run", "Karate Chop", "Leaf Blade", "Night Slash", "Poison Tail", "Psycho Cut", "Razor Leaf", "Razor Wind", "Shadow Blast", "Shadow Claw", "Sky Attack", "Slash", "Spacial Rend", "Stone Edge" ]
        high_crit = makeAPIFriendly(high_crit)


        stage = 0
        # if self.gen >= 2 and self.gen <=5: #for probability

        # MOVE STAGES
        if self.lead.moveset[mi].type.name in high_crit:
            stage += 1
            if self.gen == 2 or self.lead.moveset[mi].type.name == "10,000,000-volt-thunderbolt":
                    stage += 1

        # HELD ITEMS
        if self.lead.held_item.lower() == "razor claw" or self.lead.held_item.lower() == "scope lens":
            stage += 1
        if (self.lead.name.lower() == "farfetch'd" and self.lead.held_item == "Stick") or (self.lead.name.lower() == "chansey" and self.lead.held_item == "Lucky Punch"):
            stage += 2

        # ABILITY
        if self.lead.ability.lower() == "super luck":
            stage += 1

        ### PROBABILITY

            if stage == 0:
                if self.gen >= 2 and self.gen <=6:
                    crit_chance = randint(1,17)
                    return 2 if crit_chance == 8 else 1

                elif self.gen >= 7:
                    crit_chance = randint(1,25)
                    return 2 if crit_chance == 8 else 1

                else:
                    return 1

            elif stage == 1:
                if self.gen >= 2:
                    crit_chance = randint(1,9)
                    return 2 if crit_chance == 4 else 1
                else:
                    return 1

            elif stage == 2:
                if self.gen >= 2 and self.gen <=5:
                    crit_chance = randint(1,5)
                    return 2 if crit_chance == 2 else 1

                elif  self.gen > 5:
                    crit_chance = randint(1,3)
                    return 2 if crit_chance == 2 else 1

            elif stage >= 3:
                if self.gen > 5:
                    return 2

                elif self.gen >= 2 and self.gen <= 5:
                    if stage == 3:
                        crit_chance = randint(1,4)
                        return 2 if crit_chance == 2 else 1

                    elif stage == 4:
                        crit_chance = randint(1,3)
                        return 2 if crit_chance == 2 else 1

                else:
                    return 1




    def predictTurn(self, lookahead):
        """ returns score/dmg for each move order; we want to use the highest score next """
        total = 0
        for sim in range(lookahead):

            #TODO: calculate damage after each lookahead; we can also call nextTurn and see the total damage at the end

            att_eff = findEff()
            selected_att = att_eff.index(max(att_eff))


            #self.lead.moveset[selected_att]

    def switchPkmn(self):
        self.lead_index += 1

        if(self.lead_index >= self.team_count):
            self.lead_index = 0

        while(self.poke_team[self.lead_index].canBattle == False):
            self.lead_index += 1

        # print("Switched out " + self.lead.name + " for " + self.poke_team[self.lead_index].name)
        # print("")
        self.lead = self.poke_team[self.lead_index]


    def nextTurn(self):
        """ Trainer decides what the next best move should be """

        if(self.items != [] and self.lead.cur_hp <= self.lead.hp * .15):
            # TODO: INITIALIZE ITEMS
            # use self.items[0]
            print(" Item ")

        elif(self.team_count > 1 and (self.lead.cur_hp == self.lead.hp * .2 and self.lead.status != "NONE")):
            switchPkmn()

        else:
            # TODO: Do we want to inflict damgage, increase/decrease stats, or inflict a status move?
            #       If status, does the opponent already have a status issue?
            #       If no, go for it. If sleep, frozen, or paralyze, increase your stats and attack next turn.
            #       Check if the move inflicts damage or is a status move.


            Print("Move")
            # TODO: Do pre-calculations as to possible damage outcomes then choose the highest for next damaging move
            # TODO: when round counter goes up in battle, use the selected move then decrease pp for that move


Rai = TrainerAI("Rai", [ ["pikachu", "", 10, ["thunderbolt", "spark"], ""], ["squirtle", "", 15, ["confuse ray", "lick"], ""] ], "A", [], 4)
print(Rai)
Rai.switchPkmn()
print(Rai)
