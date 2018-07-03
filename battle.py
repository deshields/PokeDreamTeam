from trainer import TrainerAI
from poke import PokemonMember

class Battle:
    # Single Battle Only For Now, not taking player items into account
    # In double battle, use set_opponent to switch targets OR just iterate through the list of opponents

    def __init__(self, battle_type, players):
        assert(battle_type == 'SINGLE') #or battle_type == 'DOUBLE')
        assert(len(players) <= 4 and len(players) > 1)
        self.battle_type = battle_type
        self.players = players #list of trainer classes
        round = 0
        weather = "CLEAR"
        ATeam =[]
        BTeam =[]
        for p in players:
            ATeam.append(p) if p.side == "A" else BTeam.append(p)
        for A in ATeam:
            for B in BTeam:
                set_opponent(A, B)

    def __repr__(self):
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
                    p.lead.status += 1


    def takeBattleDmg(self, attacker, defender):
        ## TODO: does this belong here or in trainer class?
        # move_index = atttacker.nextMove()
        defender.lead.cur_hp = defender.lead.cur_hp - attacker.DamageCalc(2, self)
        if(defender.lead.cur_hp <= 0):
            defender.lead.canBattle = False
            defender.switchPkmn()

    def findBattleOrder(self):
        current_leads = []
        order = [len(self.players)]
        speed = 0
        speediest = 0
        for p in self.players:
            current_leads.append(p.lead)
        sorted(self.players, key=lambda poke: poke.lead.speed)




    def round(self):
        round += 1

        # we order by fastest lead
        findBattleOrder()


        for p in self.players:
            # All trainers plan - may be obselete soon
            # Faster trainer uses move first
            p.predictTurn()

            # Trainers make their decision
            ### TAKE TURNS HERE ####

            choice = p.nextTurn()
            if choice == "Item":
                print(p.name + " used an item!")
                p.useItem()
            elif choice == "Switch"
                print(p.name + " switched Pokemon!")
                p.switchPkmn()
            else:

            ### After fighting









            # Burn & Poison Damage // round by round healing


        # switch if pokemon fainted
