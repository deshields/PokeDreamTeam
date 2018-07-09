from trainer import TrainerAI, Rai, Cynthia
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

        ## Set up the teams -> A Team is the user's and B is the opponent
        for p in players:
            self.ATeam.append(p) if p.side == "A" else self.BTeam.append(p)
        for A in self.ATeam:
            for B in self.BTeam:
                set_opponent(A, B)

        self.findBattleOrder()

    def __repr__(self):
        print("Round: ", self.round)
        print("Trainers: ", self.players)

        return ""

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

        print("attacker: ", attacker)
        print("Defender: ", defender)

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

        defender.lead.cur_hp = defender.lead.cur_hp - dmg
        print(defender.lead.name + " took " + dmg + " damage!")
        if(defender.lead.cur_hp <= 0):
            print(defender.lead.name + " fainted!")
            attacker.score += 1
            defender.score -= 1
            defender.lead.canBattle = False

    def findBattleOrder(self):
        current_leads = []
        order = [len(self.players)]
        speed = 0
        speediest = 0
        for p in self.players:
            current_leads.append(p.lead)
        sorted(self.players, key=lambda poke: poke.lead.speed)


    def check_wins(self):
        a_out = 0
        b_out = 0
        for trainer  in self.players:
             if (trainer.side == 'A' and trainer.out == True): a_out += 1
             if (trainer.side == 'B' and trainer.out == True): b_out += 1
        if a_out == len(self.ATeam) and b_out == len(self.BTeam):
            print("Draw")
            return [True, '']
        elif a_out != len(self.ATeam) and b_out == len(self.BTeam):
            print("Your team wins!")
            return [True, self.ATeam]
        elif a_out == len(self.ATeam) and b_out != len(self.BTeam):
            print("Your team loses!")
            return [True, self.BTeam]

        else: return [False, '']


    def nextRound(self):

        # Check win

        print("Round: ", self.round)
        check_order = False


        self.round += 1

        for p in self.players:
            # All trainers plan - may be obselete soon
            # Faster trainer uses move first
            # p.predictTurn()
            print(p.name+"'s Turn!")

            # Trainers make their decision
            ### TAKE TURNS HERE ####

            choice = p.nextTurn()
            if p.lead.canBattle == True:
                if choice == "Item":
                    print(p.name + " used an item!")
                    p.useItem()

                elif choice == "Switch":
                    print(p.name + " switched Pokemon!")
                    p.switchPkmn()
                    print(p.lead.name + " is now in battle.")
                    check_order = True

                else:
                    self.takeBattleDmg(p, p.toAttack)


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



Sample_Battle = Battle('SINGLE', [Rai, Cynthia])
# Sample_Battle.nextRound()
print(Sample_Battle)
