from trainer import TrainerAI, Rai, Cynthia, Chu, Rai2
from poke import PokemonMember
from numpy import random

def set_opponent(TrainerA, TrainerB):
    TrainerA.opponent.append(TrainerB)
    TrainerB.opponent.append(TrainerA)



class Battle:
    # Single Battle Only For Now, not taking player items into account
    # In double battle, use set_opponent to switch targets OR just iterate through the list of opponents

    def __init__(self, battle_type, players):
        assert(battle_type == 'SINGLE') #or battle_type == 'DOUBLE')
        assert(len(players) <= 4 and len(players) > 1)
        self.battle_type = battle_type
        self.players = players #list of trainer classes
        self.round = 0
        weather = "CLEAR"
        self.ATeam =[]
        self.BTeam =[]
        self.ogA = self.ATeam
        self.ogB = self.BTeam
        self.names = [[], []]
        self.A_total = 0
        self.B_total = 0
        self.Af = 0
        self.Bf = 0
        self.over = False

        ## Set up the teams -> A Team is the user's and B is the opponent
        for p in players:
            if p.side == "A":
                self.ATeam.append(p)
                self.names[0].append(p.name)
                self.A_total += p.team_count

            else:
                 self.BTeam.append(p)
                 self.names[1].append(p.name)
                 self.B_total += p.team_count

        for A in self.ATeam:
            for B in self.BTeam:
                set_opponent(A, B)
                A.toAttack = B
                B.toAttack = A

        print("Battle of ", self.names[0], " vs. ", self.names[1])


        self.findBattleOrder()

    # def __repr__(self):
    #     print("Round: ", self.round)
    #     print("Trainers: ", self.players)
    #
    #     return ""

    def takeStatusDmg(self):
        for p in self.players:
            if p.lead.status[0] == "BURNED" or p.lead.status[0] == "POISONED":
                if p.gen == 1:
                    p.lead.cur_hp - (1/16 * p.lead.hp)
                else:
                    p.lead.cur_hp - (1/8 * p.lead.hp)
            elif p.lead.status[0] == "BADLY POISONED":
                    p.lead.cur_hp - (1/16 * p.lead.status[1] * p.lead.hp)
                    p.lead.status[1] += 1


    def takeBattleDmg(self, attacker, defender):
        """ Calculates the damage between two pokemon; NOTE: it does NOT account for moves like Surf in a double Battle """
        # move_index = atttacker.nextMove()

        if "PARALYZED" in attacker.lead.status:
            if random.randint(4) == 2:
                print(attacker.lead.name + " is paralyzed!")
                return

        elif "FROZEN" in attacker.lead.status:
            if random.randint(5) == 2:
                print(attacker.lead.name + " thawed out!")
                attacker.lead.status[0] = "NONE"
                attacker.lead.status[-1] = -1
            else:
                print(attacker.lead.name + " is frozen solid!")
                return

        elif "SLEEP" in attacker.lead.status:
            if attacker.lead.status[1] >= 3 or (attacker.lead.status[1] >= 1 and random.randint(3) == 2):
                print(attacker.lead.name + " woke up!")
                attacker.lead.status[0] = "NONE"
                attacker.lead.status[-1] = -1
            else:
                print(attacker.lead.name + " is fast asleep.")
                return


        for sub in defender.lead.sub_status:
            if sub[0] == "PROTECTED" or sub[0] == "AIRBORNE":
                print("The attack missed!")
                return

        dmg = attacker.predictDMG(self)[1]
        if defender.lead.canBattle == True:
            defender.lead.cur_hp = defender.lead.cur_hp - dmg
            print(defender.lead.name + " took " + str(dmg) + " damage!")
            if(defender.lead.cur_hp <= 0):

                attacker.score += 1
                defender.score -= 1
                defender.lead.canBattle = False
                print(defender.lead.name + " fainted!")
                defender.faintCount += 1
                if defender.side == "A":
                    self.Af +=1
                else:
                    self.Bf +=1
                self.check_wins()

    def getSpeed(self, player):
        return player.lead.speed

    def findBattleOrder(self):
        current_leads = []
        order = [len(self.players)]
        speed = 0
        speediest = 0
        for p in self.players:
            current_leads.append(p.lead)

        self.players.sort(key=self.getSpeed, reverse=True)

        # print(self.players)


    def check_wins(self):

        if  self.Af == self.A_total and self.Bf == self.B_total:
            print("Draw")
            self.over = True
            return 'None'
        elif self.Af != self.A_total and self.Bf == self.B_total:
            print("Your team wins!")
            self.over = True
            return self.ATeam
        elif self.Af == self.A_total and self.Bf != self.B_total:
            print("Your team loses!")
            self.over = True
            return self.BTeam




    def nextRound(self):

        # Check win

        self.round += 1
        print("")
        print("Round: ", self.round)
        check_order = False
        if self.over == True:
            print("---- Battle OVER ----")
            return



        for p in self.players:
            # All trainers plan - may be obselete soon
            # Faster trainer uses move first


            if p.lead.canBattle == True and p.out == False:
                # self.check_wins()
                print(p.name+"'s Turn!")

            # Trainers make their decision
            ### TAKE TURNS HERE ####

                choice = p.nextTurn()

                if choice == "Item":
                    print(p.name + " used an item!")
                    p.useItem()

                elif choice == "Switch":
                    print(p.name + " switched Pokemon!")
                    p.switchPkmn()
                    print(p.lead.name + " is now in battle.")
                    check_order = True

                else:
                    chec = p.selectOpponent()
                    if chec != "miss":
                        self.takeBattleDmg(p, p.toAttack)
                    else:
                        print("But there was no target.")


            ### After fighting

        self.takeStatusDmg()
        if check_order:
            self.findBattleOrder()
            check_order = False
            # Burn & Poison Damage // round by round healing


        # switch if pokemon fainted
        for p in self.players:
            if p.lead.canBattle == False:
                p.switchPkmn()
                # self.check_wins()
            if p.out == True and p.removed == False:
                if p.side == "A":
                    self.ATeam.remove(p)
                    for o in self.BTeam:
                        o.opponent.remove(p)
                else:
                    self.BTeam.remove(p)
                    for o in self.ATeam:
                        o.opponent.remove(p)
                p.removed = True
                print("~~~~~~~~~ " + p.name + " is removed from battle!")



Sample_Battle = Battle('SINGLE', [Rai, Chu, Cynthia, Rai2])
# print(Rai.lead)
# print(Cynthia.lead)
# Sample_Battle.nextRound()
# Sample_Battle.nextRound()
# print(Sample_Battle)
