### For Enemy Trainer Single Battle

import csv
import pandas as pd
import pokebase as pb
from numpy import random

from poke import PokemonMember

def makeAPIFriendly(l_string):
    """ Makes it easier for API to read
        l_string = list of strings """

    for i in range(len(l_string)):
        l_string[i] = l_string[i].replace(" ", "-")
        l_string[i] = l_string[i].lower()

    return l_string

def makePokemon():
    # For JSON data in form list
    name = request.form['name']
    lvl = request.form['lvl']
    moves = request.form['moves']
    item = request.form['item']
    Pokemon = PokemonMember(name, '', lvl, moves, item)


class TrainerAI:

    def __init__(self, name, team, side, items, generation):

        assert(side == "A" or side == "B")
        assert(team != [])
        #assert(region == "KANTO" or region == "JOHTO" or region == "HOENN" or region == "SINNOH" or region == "UNOVA")
        self.name = name # String - optional
        self.team = team # List of strings or Pokemon Objects [ ["pikachu", "", 10, ["thunderbolt", "spark"], ""], ["squirtle", "", 15, ["confuse ray", "lick"], ""] ]
        self.team_count = len(team)
        self.poke_team = []
        self.makeTeam()
        self.lead = self.poke_team[0]
        self.lead_index = 0
        self.items = items # if use is true, list of strings, otherwise null
        self.gen = generation # String - optional
        self.opponent = []
        self.allies = []
        self.toAttack = None # Trainer class
        self.side = side # 'A' or 'B'
        self.type_list = None

        self.prev_decision = ["None", "None"] # will update to ["Move", "Flamethrower"], ["Item", "Potion"], ["Switch", "Pokemon-Swapped-In"]
        self.out = False # gets set to True if all PKMN are at 0
        self.removed = False
        self.score = 0 # +1 for every opponent Pokemon defeated -1 for every owned pokemon defeated
        self.faintCount = 0

    def __repr__(self):

        print("Trainer: " + self.name)
        print("Leading Pokemon: " + self.lead.name)
        print("Current Health: " + str(self.lead.cur_hp) + " / " + str(self.lead.hp))
        print("Gen: " + str(self.gen))
        print("Opponent: ", self.opponent[0].name)
        return ""

    def makeTeam(self):
        """ Converts string team input to PokemonMember class """
        for p in self.team:
            self.poke_team.append(PokemonMember(p[0], p[1], p[2], p[3], p[4]))

    def findEff(self):
        """ Finds the effectiveness of the user's leading pokemon's moveset against the type of the opponent.
            Returns a list
         """
        move_eff = []
        opp_eff = []
        for opp in self.opponent:
            for i in range(len(self.lead.moveData)):
                opp_eff.append(self.lead.checkEffectiveness(i, opp.lead.type))


                # if len(self.toAttack.lead.type) == 2:
            move_eff.append(opp_eff)
            opp_eff = []

        return move_eff

    def OpponentsCanBattle(self):
        """ Check if the opponents can all battle """

        out = 0
        for o in self.opponent:
            if (o.lead.canBattle) != True or o.out:
                out += 1
        if out == len(self.opponent):
            return False
        else:
            return True

    def selectOpponent(self):

        """ Select who to attack next """

        self.type_list = self.findEff()
        if len(self.opponent) > 1:

            all_max_hits = [x for x in self.type_list if x == max(self.type_list)]
            # print("all_max_hits: ", all_max_hits)
            all_ind = [x for x in range(len(all_max_hits)) if (self.opponent[x].lead.canBattle == True)]
            # print("all_ind: ", all_ind)
            if all_ind == []:
                return "miss"

            self.current_target = random.choice(all_ind)
            #mex2 = mex.index(max(mex))
            # print("Target ind:", target)
            #print("M2",mex2)
            self.toAttack = self.opponent[self.current_target]
        else:
            self.current_target = 0
            self.toAttack = self.opponent[0]


    def DamageCalc(self, mi, battle):
        """ Calculate damage against opponent
        https://bulbapedia.bulbagarden.net/wiki/Damage ,
        mi is the move index, battle is the battle class it's in"""

        # Type effectiveness and target
        #self.selectOpponent()

        # print("Testing: " + self.lead.name + " used " + self.lead.moveData[mi].name + " on " + self.toAttack.lead.name)

        if self.lead.moveData[mi].target.name != 'selected-pokemon':
            targets = 0.75
        else:
            targets = 1

        if self.lead.moveData[mi].damage_class.name == 'physical':
            dmg = ( ( ( ( (2 * self.lead.level)/5 ) + 2 ) * self.lead.moveData[mi].power * (self.lead.att / self.toAttack.lead.defe) ) / 50 ) + 2
            burn = 0.5 if self.lead.status[0] == "BURNED" else 1

        else:
            dmg = ( ( ( ( (2 * self.lead.level)/5 ) + 2 ) * self.lead.moveData[mi].power * (self.lead.spatt / self.toAttack.lead.spdef) ) / 50 ) + 2
            burn = 1

        ### Modifier Calculations

        # Weather
        if (self.lead.moveData[mi].type.name == 'fire' and battle.weather == "SUNNY") or (self.lead.moveData[mi].type.name == 'water' and battle.weather == "RAIN"):
            w = 1.5
        elif (self.lead.moveData[mi].type.name == 'water' and battle.weather == "SUNNY") or (self.lead.moveData[mi].type.name == 'fire' and battle.weather == "RAIN"):
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
        stab = 1.5 if self.lead.moveData[mi].type.name in self.lead.type else 1

        # print(self.type_list, "current_target: ", self.current_target, "mi: ", mi)
        t = self.type_list[self.current_target][mi] # TODO: For now, always attack the opponent in index 0

        # THIS MODIFIER IS ONLY TO BE USED FOR SINGLE BATTLES SINCE THERE IS ONE TARGET
        modifier = targets * w * self.isCrit(mi) * r * stab * t * burn # * other ( * badge for gen ii)

        #print("Total damage: " + str(modifier * dmg))

        return round(modifier * dmg)



    def isCrit(self, mi):
        """ Returns 2 if crit, if not return 1 """

        high_crit = ["10,000,000 Volt Thunderbolt", "Aeroblast", "Air Cutter", "Attack Order", "Blaze Kick", "Crabhammer", "Cross Chop", "Cross Poison", "Drill Run", "Karate Chop", "Leaf Blade", "Night Slash", "Poison Tail", "Psycho Cut", "Razor Leaf", "Razor Wind", "Shadow Blast", "Shadow Claw", "Sky Attack", "Slash", "Spacial Rend", "Stone Edge" ]
        high_crit = makeAPIFriendly(high_crit)


        stage = 0
        # if self.gen >= 2 and self.gen <=5: #for probability

        # MOVE STAGES
        if self.lead.moveData[mi].type.name in high_crit:
            stage += 1
            if self.gen == 2 or self.lead.moveData[mi].type.name == "10,000,000-volt-thunderbolt":
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
                crit_chance = random.randint(1,17)
                if crit_chance == 8:
                    print("Critical hit!")
                    return 2
                else: return 1

            elif self.gen >= 7:
                crit_chance = random.randint(1,25)
                if crit_chance == 8:
                    print("Critical hit!")
                    return 2
                else: return 1

            else:
                return 1

        elif stage == 1:
            if self.gen >= 2:
                crit_chance = random.randint(1,9)
                if crit_chance == 4:
                    print("Critical hit!")
                    return 2
                else: return 1
            else:
                return 1

        elif stage == 2:
            if self.gen >= 2 and self.gen <=5:
                crit_chance = random.randint(1,5)
                if crit_chance == 2:
                    print("Critical hit!")
                    return 2
                else: return 1

            elif  self.gen > 5:
                crit_chance = random.randint(1,3)
                if crit_chance == 2:
                    print("Critical hit!")
                    return 2
                else: return 1

        elif stage >= 3:
            if self.gen > 5:
                print("Critical hit!")
                return 2

            elif self.gen >= 2 and self.gen <= 5:
                if stage == 3:
                    crit_chance = random.randint(1,4)
                    if crit_chance == 2:
                        print("Critical hit!")
                        return 2
                    else: return 1

                elif stage == 4:
                    crit_chance = random.randint(1,3)
                    if crit_chance == 2:
                        print("Critical hit!")
                        return 2
                    else: return 1

            else:
                return 1


    def predictDMG(self, battle):
        """ returns score/dmg for each move order; we want to use the highest score next """
        # # OPTIMIZE: if they're all the same pokemon and no status or pokemon switch has occurred, there's no need to
            # always recalculate hits. We could save how much each does, and if the damage is equal or very similar between moves
            # alternate or move to the next best move

        # lookahead would be no greater than one
        score = [0 for x in range(len(self.lead.moveData))]
        ogToAttack = self.toAttack
        for sim in range(len(self.lead.moveData)):
            if self.lead.moveData[sim].power != None and self.lead.pp[sim] > 0:
                if self.lead.moveData[sim].target.name == 'selected-pokemon':
                    if self.toAttack.lead.canBattle == True:
                        score[sim] = self.DamageCalc(sim, battle)
                elif self.lead.moveData[sim].target.name == 'all-opponents':
                    total = 0
                    for o in self.opponent:
                        self.toAttack = o
                        total += self.DamageCalc(sim, battle)
                    score[sim] = total
                elif self.lead.moveData[sim].target.name == 'all-other-pokemon':
                    total = 0

                    for t in battle.players:
                        if t != self:
                            if t.side == self.side:
                                self.toAttack = t
                                total -= 2 * self.DamageCalc(sim, battle)
                            else:
                                self.toAttack = t
                                total += self.DamageCalc(sim, battle)
            else:
                score[sim] = -1

        self.toAttack = ogToAttack

        print(self.lead.name + " used " + str(self.lead.moves[score.index(max(score))]) + " on " + self.toAttack.lead.name + "!")


        self.lead.pp[score.index(max(score))] -= 1

        # if max(score) == 0:
        #     print("The attack missed!")
        #     return [-2, 'no target']

        return [score.index(max(score)), max(score), self.lead.moveData[score.index(max(score))].target.name]

    def switchPkmn(self):
        """ Switches leading pokemon """
        if len(self.team) > 1:
            if self.faintCount >= self.team_count:
                self.out = True
                return
            else:
                self.lead_index += 1
                if(self.lead_index >= self.team_count):
                    self.lead_index = 0
                while(self.poke_team[self.lead_index].canBattle == False):
                    if(self.lead_index >= self.team_count):
                        self.lead_index = 0
                    else:
                        self.lead_index += 1

        else:
            if self.lead.canBattle == False:
                self.out = True


        # print("Switched out " + self.lead.name + " for " + self.poke_team[self.lead_index].name)
        # print("")
        if self.out == False:
            print(self.name + " sent out " + self.poke_team[self.lead_index].name + "!")
            self.lead = self.poke_team[self.lead_index]

    def useItem(self, item):
        if "potion" in self.items:
            self.lead.cur_hp += 20
            if self.lead.cur_hp > self.lead.hp:
                self.lead.cur_hp = self.lead.hp
            self.items[index("potion")] = ""

        elif "full restore" in self.items:
            self.lead.cur_hp = self.lead.hp
            self.items[index("full restore")] = ""

    def nextTurn(self):
        """ Trainer decides what the next best move should be """

        if(self.items != [] and self.lead.cur_hp <= self.lead.hp * .15):
            #useItem(self.items[0])
            return "Item"

        elif(self.team_count > 1 and (self.lead.cur_hp == self.lead.hp * .2 and self.lead.status[0] != "NONE")):
            #switchPkmn()
            return "Switch"

        else:
            # TODO: Do we want to inflict damgage, increase/decrease stats, or inflict a status move?
            #       If status, does the opponent already have a status issue?
            #       If no, go for it. If sleep, frozen, or paralyze, increase your stats and attack next turn.
            #       Check if the move inflicts damage or is a status move.

            # TODO: Do pre-calculations as to possible damage outcomes then choose the highest for next damaging move
            # TODO: when round counter goes up in battle, use the selected move then decrease pp for that move

            return "Fight"


### Presets

Rai = TrainerAI("Rai", [ ["pikachu", "", 5, ["thunderbolt", "spark"], ""], ["squirtle", "", 10, ["confuse ray", "lick"], ""] ], "A", [], 4)
Chu = TrainerAI("Chu", [ ["minun", "", 65, ["thunderbolt", "iron tail"], ""], ["zubat", "", 70, ["confuse ray", "lick"], ""] ], "A", [], 4)
Rai2 = TrainerAI("Rai-2", [ ["shinx", "", 5, ["thunderbolt", "spark"], ""], ["gastly", "", 10, ["confuse ray", "lick"], ""] ], "B", [], 4)
Cynthia = TrainerAI("Cynthia", [ ["spiritomb", "", 61, ["dark pulse", "embargo", "psychic", "silver wind"], ""],["garchomp", "", 66, ["brick break" , "dragon rush", "earthquake", "giga impact"], ""] ], "B", [], 4)
