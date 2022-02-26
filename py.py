import math
import random

class Character(object):

    def __init__(self, name, MAX_hp, base_speed, priority="Normal", mindset_multiplier=1.0, move=''):
        self.MAX_hp = MAX_hp
        self.base_hp = MAX_hp
        self.base_speed = base_speed
        self.priority = priority
        self.mindset_multiplier = mindset_multiplier
        self.name = name

        self.move_pool = {}

    def __repr__(self):
        return "{self.name} - {self.base_hp} / {self.MAX_hp} HP, {self.mindset_multiplier} mindset, {self.base_speed} speed".format(self=self)

class Move(object):

    def __init__(self, description="", self_damage=0, damage=0, mindset_multiplier=1.0, opponent_mindset_multiplier=1.0, speed_boost=0, opponent_speed_boost=0, priority="Normal"):
        self.__doc__ = description
        self.self_damage = self_damage
        self.damage = damage
        self.mindset_multiplier = mindset_multiplier
        self.opponent_mindset_multiplier = opponent_mindset_multiplier
        self.speed_boost = speed_boost
        self.opponent_speed_boost = opponent_speed_boost
        self.priority = priority

    def __call__(self, user=None, opponent=None):
        if user is not None:
            user.priority = self.priority
            user.mindset_multiplier *= self.mindset_multiplier
            user.base_speed += self.speed_boost
            user.base_hp -= math.floor(self.self_damage *
                                           user.mindset_multiplier)
            user.base_hp = min(max(user.base_hp, 0), user.MAX_hp)

        if opponent is not None:
            opponent.mindset_multiplier *= self.opponent_mindset_multiplier
            opponent.base_speed += self.speed_boost
            opponent.base_hp -= math.floor(self.damage *
                                           user.mindset_multiplier)
            opponent.base_hp = min(max(opponent.base_hp, 0), opponent.MAX_hp)

class Berserker(Character):

    def __init__(self):
        Character.__init__(self, "Berserker", 250, 75)
        self.move_pool = {"1": Move(" Jab - A fast, light attack. Does 30 Basic Damage to Opponent",
                                    damage=30, priority="Fast"),
                          "2": Move(" Haymaker - A Slow, strong attack. Does 65 Base to Opponent and 30 Base Damage to User",
                                    self_damage=30, damage=65, priority="Slow"),
                          "3": Move(" PumpUp - Normal speed. Improves the Mindset of the User ( x 1.25 )",
                                    mindset_multiplier=1.25)}

class Philosopher(Character):

    def __init__(self):
        Character.__init__(self, "Philosopher", 220, 80)
        self.move_pool = {"1": Move(" Insight - A Normal speed move. Restores up to a Base of 30 HP to User",
                                    self_damage=-30),
                          "2": Move(" Pedantry - A Normal-speed attack. Does 40 Base Damage to the Opponent",
                                    damage=40),
                          "3": Move(" Research - A Normal-speed move. Improves the Mindset of the User (x 1.35)",
                                    mindset_multiplier=1.35)}

class Trickster2(Character):

    class Bag_o_tricks(Move):

        def __call__(self, user, opponent):
            self.damage = random.uniform(-1, 1) * 100
            self.self_damage = random.uniform(-1, 1) * 50
            Move.__call__(self, user, opponent)

    class Swapper(Move):

        def __call__(self, user, opponent):
            user.priority = self.priority
            user.base_hp, opponent.base_hp = opponent.base_hp, user.base_hp
            user.MAX_hp, opponent.MAX_hp = opponent.MAX_hp, user.MAX_hp

    def __init__(self):
        Character.__init__(self, "Trickster", 175, 100)
        self.move_pool = {"1": Trickster2.Bag_o_tricks(" Bag-O-Tricks - A Normal-speed move. Increases or Decreases Opponent HP anywhere from 0 to 100 and User HP from 0 to 50"),
                          "2": Move(" Tease - A Normal-speed move. Reduces the Mindset of the Opponent (x 0.8)",
                                    mindset_multiplier=1.05, opponent_mindset_multiplier=0.8),
                          "3": Trickster2.Swapper(" Swapper - A Normal-speed move. Swaps the User HP with the Opponent HP")}
        import random
import math
import sys
import os
import time
from characters import *

class Game(object):

    mode_options = {'1':('Player 1','CPU'), '2':('CPU 1','CPU 2'), '3':('Player 1','Player 2')}
    game_mode = '' # Preallocation
    game_mode_choice = '' # Preallocation and Stroage

    character_options = {'1':Berserker, '2':Philosopher, '3':Trickster2}
    move_order = '' # Preallocation

    def __init__(self):
        """ """

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def introduction(self):
        game.clear_screen()print """
        ______       ______  _         _      _              
        | ___ \      |  ___|(_)       | |    | |             
        | |_/ /_   _ | |_    _   __ _ | |__  | |_  ___  _ __ 
        |  __/| | | ||  _|  | | / _` || '_ \ | __|/ _ \| '__|
        | |   | |_| || |    | || (_| || | | || |_|  __/| |   
        \_|    \__, |\_|    |_| \__, ||_| |_| \__|\___||_|   
                __/ |            __/ |                       
               |___/            |___/                        """
        time.sleep(1)
        game.clear_screen()
    
    def choose_game_mode(self):
        while True:
            self.game_mode_choice = raw_input("What versus mode would you like to play: \
                \n1) Player v. CPU \
                \n2) CPU1 v. CPU2 \
                \n3) Player 1 v. Player 2 \
                \n0) Exit Game.\n\n")

            game.clear_screen()

            if self.game_mode_choice == '0':
                sys.exit()
            try:
                self.game_mode = self.mode_options[ self.game_mode_choice ]
                return None
            except KeyError:
                print "Please choose one of the listed options.\n"
                time.sleep(1)

    def character_selection(self,controller_index):
        while True:
            character_choice = raw_input("Who should " + self.game_mode[controller_index] + " play as:\
                \n1) The Berserker\
                \n2) The Philosopher\
                \n3) The Trickster\
                \n4) Random\
                \n\
                \n0) Exit Game.\n\n")

            game.clear_screen()

            if character_choice == '0':
                sys.exit()
            elif character_choice == '4':
                character_choice = str (random.randint(1,3))

            try:
                return self.character_options[ character_choice ]
            except KeyError:
                print "Please choose one of the listed options.\n"
                time.sleep(1)

    def hp_check(self,controller_1, controller_2):
        if controller_1.base_hp <= 0:
            if controller_2.base_hp >0:
                self.clear_screen
                print "Controller 2 Wins!"
                sys.exit()
            else:
                self.clear_screen
                print "It's a Draw!!!"
                sys.exit()
        elif controller_2.base_hp <= 0:
            self.clear_screen
            print "Controller 1 Wins!"
            sys.exit()
        else:
            pass

    def player_choose_move(self,controller,controller_index):
        while True:
            move_choice = raw_input(self.game_mode[controller_index] + ", choose your move:\
            \n1)" + controller.move_pool['1'].__doc__ + "\
            \n2)" + controller.move_pool['2'].__doc__ + "\
            \n3)" + controller.move_pool['3'].__doc__ + "\n\n")

            try:
                controller.move = controller.move_pool[move_choice]
                return None
            except KeyError:
                game.clear_screen()
                print "Please choose one of the listed options.\n"
                time.sleep(1)

    def comp_choose_move(self,controller):
        controller.move = controller.move_pool[ random.choice( ['1','2','3'] )]

    def priority_and_speed_check(self,controller1,controller2):
        if controller1.priority > controller2.priority:
            return True
        elif controller1.priority == controller2.priority:
            if controller1.base_speed > controller2.base_speed:
                return True
            elif controller1.base_speed == controller2.base_speed:
                return bool ( random.choice([0,1]) )
            else:
                return False
        else:
            return False

    def update(self,controller1,controller2):
        print self.game_mode[0], " HP:", str(Player_1.base_hp), "\n", self.game_mode[0], "Mindset: x", str(Player_1.mindset_multiplier), "\n"
        print self.game_mode[1], " HP:", str(Player_2.base_hp), "\n", self.game_mode[1], "Mindset: x", str(Player_2.mindset_multiplier), "\n"
        print "\n\n"

    def move_collection(self,controller1,controller2):
        if self.game_mode_choice == '1':
            self.update(Player_1,Player_2)
            self.player_choose_move(Player_1,0)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_2)
            self.clear_screen()

        elif self.game_mode_choice == '2':
            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_1)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_2)
            self.clear_screen()

        else:
            self.update(Player_1,Player_2)
            self.player_choose_move(Player_1,0)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.player_choose_move(Player_2,1)
            self.clear_screen()

    def move_application(self,controller1,controller2):
        if self.priority_and_speed_check(Player_1,Player_2):
            Player_1.move(Player_1,Player_2)
            self.hp_check(Player_1,Player_2)

            Player_2.move(Player_2,Player_1)
            self.hp_check(Player_1,Player_2)
        else:
            Player_2.move(Player_2,Player_1)
            self.hp_check(Player_1,Player_2)

            Player_1.move(Player_1,Player_2)
            self.hp_check(Player_1,Player_2)

game = Game()
game.introduction()
game.choose_game_mode()

( Player_1, Player_2 ) = ( game.character_selection(0)(), game.character_selection(1)() )
while True:
    game.move_collection(Player_1,Player_2)
    game.move_application(Player_1,Player_2)
    import math
import random

class Character(object):

    def __init__(self, name, MAX_hp, base_speed, priority="Normal", mindset_multiplier=1.0, move=''):
        self.MAX_hp = MAX_hp
        self.base_hp = MAX_hp
        self.base_speed = base_speed
        self.priority = priority
        self.mindset_multiplier = mindset_multiplier
        self.name = name

        self.move_pool = {}

    def __repr__(self):
        return "{self.name} - {self.base_hp} / {self.MAX_hp} HP, {self.mindset_multiplier} mindset, {self.base_speed} speed".format(self=self)

class Move(object):

    def __init__(self, description="", self_damage=0, damage=0, mindset_multiplier=1.0, opponent_mindset_multiplier=1.0, speed_boost=0, opponent_speed_boost=0, priority="Normal"):
        self.__doc__ = description
        self.self_damage = self_damage
        self.damage = damage
        self.mindset_multiplier = mindset_multiplier
        self.opponent_mindset_multiplier = opponent_mindset_multiplier
        self.speed_boost = speed_boost
        self.opponent_speed_boost = opponent_speed_boost
        self.priority = priority

    def __call__(self, user=None, opponent=None):
        if user is not None:
            user.priority = self.priority
            user.mindset_multiplier *= self.mindset_multiplier
            user.base_speed += self.speed_boost
            user.base_hp -= math.floor(self.self_damage *
                                           user.mindset_multiplier)
            user.base_hp = min(max(user.base_hp, 0), user.MAX_hp)

        if opponent is not None:
            opponent.mindset_multiplier *= self.opponent_mindset_multiplier
            opponent.base_speed += self.speed_boost
            opponent.base_hp -= math.floor(self.damage *
                                           user.mindset_multiplier)
            opponent.base_hp = min(max(opponent.base_hp, 0), opponent.MAX_hp)

class Berserker(Character):

    def __init__(self):
        Character.__init__(self, "jan pi pakala nasa", 250, 75)
        self.move_pool = {"1": Move(" utala lili luka - tenpo lili la, ona li pakala 30 e jan ante.",
                                    damage=30, priority="Fast"),
                          "2": Move(" utala sijelo - tenpo suli la, ona li pakala 50 e jan ante li pakala 30 e sijelo sama",
                                    self_damage=30, damage=50, priority="Slow"),
                          "3": Move(" wawa sewi - wawa sama li kama sewi ( x 1.25 ).",
                                    mindset_multiplier=1.25)}

class Philosopher(Character):

    def __init__(self):
        Character.__init__(self, "jan pi sona mute", 220, 80)
        self.move_pool = {"1": Move(" sona pona - ona li pona 30 e sijelo sama",
                                    self_damage=-30),
                          "2": Move(" toki mute pi ike mute - ona li pakala 40 e jan ante.",
                                    damage=40),
                          "3": Move(" sona sewi - sona ona li kama sewi. (x 1.35)",
                                    mindset_multiplier=1.35)}

class Trickster2(Character):

    class Bag_o_tricks(Move):

        def __call__(self, user, opponent):
            self.damage = random.uniform(-1, 1) * 100
            self.self_damage = random.uniform(-1, 1) * 50
            Move.__call__(self, user, opponent)

    class Swapper(Move):

        def __call__(self, user, opponent):
            user.priority = self.priority
            user.base_hp, opponent.base_hp = opponent.base_hp, user.base_hp
            user.MAX_hp, opponent.MAX_hp = opponent.MAX_hp, user.MAX_hp

    def __init__(self):
        Character.__init__(self, "jan pi powe nasa", 175, 100)
        self.move_pool = {"1": Trickster2.Bag_o_tricks(" nasin nasa - ona li ante e [-100,100] pi jan ante e [-50,50] pi jan sama."),
                          "2": Move(" ike nasa - ona li ike e lawa pi jan ante (x 0.8) li pona e lawa sama (x 1.05)",
                                    mindset_multiplier=1.05, opponent_mindset_multiplier=0.8),
                          "3": Trickster2.Swapper(" sijelo ante - ona li ante sama e sijelo pi jan ante e sijelo pi jan sama.")}
import random
import math
import sys
import os
import time
from tp_characters_test import *

class Game(object):

    mode_options = {'1':('jan 1','jan ilo'), '2':('jan ilo 1','jan ilo 2'), '3':('jan 1','jan 2')}
    game_mode = '' # Preallocation
    game_mode_choice = '' # Preallocation and Stroage

    character_options = {'1':Berserker, '2':Philosopher, '3':Trickster2}
    move_order = '' # Preallocation

    def __init__(self):
        """ """

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def introduction(self):
        game.clear_screen()
        print """
				_________ _______  _                      _________ _______  _        _______ 
				\__    _/(  ___  )( (    /|      |\     /|\__   __/(  ___  )( \      (  ___  )
				   )  (  | (   ) ||  \  ( |      | )   ( |   ) (   | (   ) || (      | (   ) |
				   |  |  | (___) ||   \ | |      | |   | |   | |   | (___) || |      | (___) |
				   |  |  |  ___  || (\ \) |      | |   | |   | |   |  ___  || |      |  ___  |
				   |  |  | (   ) || | \   |      | |   | |   | |   | (   ) || |      | (   ) |
				|\_)  )  | )   ( || )  \  |      | (___) |   | |   | )   ( || (____/\| )   ( |
				(____/   |/     \||/    )_)      (_______)   )_(   |/     \|(_______/|/     \|
                                                                              					"""
        time.sleep(1)
        game.clear_screen()
    
    def choose_game_mode(self):
        while True:
            self.game_mode_choice = raw_input("sina pali musi e seme: \
                \n1) sina u. jan ilo \
                \n2) jan ilo 1 u. jan ilo 2 \
                \n3) jan 1 u. jan 2 \
                \n0) tawa.\n\n")

            game.clear_screen()

            if self.game_mode_choice == '0':
                sys.exit()
            try:
                self.game_mode = self.mode_options[ self.game_mode_choice ]
                return None
            except KeyError:
                print "ala. wile sina e ike. sina ante e wile sina.\n"
                time.sleep(1)

    def character_selection(self,controller_index):
        while True:
            character_choice = raw_input(self.game_mode[controller_index] + " li wile kepeken:\
                \n1) jan pi pakala nasa\
                \n2) jan pi sona mute\
                \n3) jan pi powe nasa\
                \n4) nasin pi sona ala\
                \n\
                \n0) tawa.\n\n")

            game.clear_screen()

            if character_choice == '0':
                sys.exit()
            elif character_choice == '4':
                character_choice = str (random.randint(1,3))

            try:
                return self.character_options[ character_choice ]
            except KeyError:
                print "ala. wile sina e ike. sina ante e wile sina.\n"
                time.sleep(1)

    def hp_check(self,controller_1, controller_2):
        if controller_1.base_hp <= 0:
            if controller_2.base_hp >0:
                self.clear_screen
                print "jan 2 li kama sewi!"
                sys.exit()
            else:
                self.clear_screen
                print "jan tu li lon sama!!!"
                sys.exit()
        elif controller_2.base_hp <= 0:
            self.clear_screen
            print "jan 1 li kama sewi!"
            sys.exit()
        else:
            pass

    def player_choose_move(self,controller,controller_index):
        while True:
            move_choice = raw_input("o, " + self.game_mode[controller_index] + ", sina wile e seme:\
            \n1)" + controller.move_pool['1'].__doc__ + "\
            \n2)" + controller.move_pool['2'].__doc__ + "\
            \n3)" + controller.move_pool['3'].__doc__ + "\n\n")

            try:
                controller.move = controller.move_pool[move_choice]
                return None
            except KeyError:
                game.clear_screen()
                print "ala. wile sina e ike. sina ante e wile sina.\n"
                time.sleep(1)

    def comp_choose_move(self,controller):
        controller.move = controller.move_pool[ random.choice( ['1','2','3'] )]

    def priority_and_speed_check(self,controller1,controller2):
        if controller1.priority > controller2.priority:
            return True
        elif controller1.priority == controller2.priority:
            if controller1.base_speed > controller2.base_speed:
                return True
            elif controller1.base_speed == controller2.base_speed:
                return bool ( random.choice([0,1]) )
            else:
                return False
        else:
            return False

    def update(self,controller1,controller2):
        print "sijelo pi", self.game_mode[0], ":", str(Player_1.base_hp), "\n", self.game_mode[0], "sona lawa: x " + str(Player_1.mindset_multiplier), "\n"
        print "sijelo pi", self.game_mode[1], ":", str(Player_2.base_hp), "\n", self.game_mode[1], "sona lawa: x " + str(Player_2.mindset_multiplier), "\n"
        print "\n\n"

    def move_collection(self,controller1,controller2):
        if self.game_mode_choice == '1':
            self.update(Player_1,Player_2)
            self.player_choose_move(Player_1,0)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_2)
            self.clear_screen()

        elif self.game_mode_choice == '2':
            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_1)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.comp_choose_move(Player_2)
            self.clear_screen()

        else:
            self.update(Player_1,Player_2)
            self.player_choose_move(Player_1,0)
            self.clear_screen()

            self.update(Player_1,Player_2)
            self.player_choose_move(Player_2,1)
            self.clear_screen()

    def move_application(self,controller1,controller2):
        if self.priority_and_speed_check(Player_1,Player_2):
            Player_1.move(Player_1,Player_2)
            self.hp_check(Player_1,Player_2)

            Player_2.move(Player_2,Player_1)
            self.hp_check(Player_1,Player_2)
        else:
            Player_2.move(Player_2,Player_1)
            self.hp_check(Player_1,Player_2)

            Player_1.move(Player_1,Player_2)
            self.hp_check(Player_1,Player_2)

game = Game()
game.introduction()
game.choose_game_mode()

( Player_1, Player_2 ) = ( game.character_selection(0)(), game.character_selection(1)() )
while True:
    game.move_collection(Player_1,Player_2)
    game.move_application(Player_1,Player_2)
