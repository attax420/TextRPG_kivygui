from random import choice 
from time import sleep
import os, sys
from platform import system

if system().lower() == 'windows':
    os.system('color')
if system().lower() == 'linux':
    import readline

# ######### MAP ######### #
class GameMap:
    def __init__(self): 
        self.map_string = ''       
        self.map = []
        self.map_x = 10
        self.map_y = 30
        self.player_pos_x = int(choice(range(self.map_x -1)))
        self.player_pos_y = int(choice(range(self.map_y -1)))        
        self.boss_x = int(choice(range(self.map_x -1)))
        self.boss_y = int(choice(range(self.map_y -1)))        
        for i in range(self.map_y):
            self.map.append([])
            for j in range(self.map_x):
                self.map[i].append(-1)

    def position_update(self):
        run = True        
        while run == True:
            if self.boss_x != self.player_pos_x or self.boss_y != self.player_pos_y:                
                       self.map[self.player_pos_y][self.player_pos_x] = ('█')
                       run = False
            else:
                self.player_pos_x = int(choice(range(self.map_x -1)))
                self.player_pos_y = int(choice(range(self.map_y -1)))  
                continue
    
    def map_to_string(self):
        self.map_string = ''
        for i in range(self.map_y):
            self.map_string +='|'
            for j in range(self.map_x):
                map_string_value = str(self.map[i][j])
                self.map_string += map_string_value + ' | '                
            self.map_string += '\n'      

    def print_map(self):
        self.map_to_string()
        print(self.map_string)
    
    def randomize_map(self):
        for i in range(self.map_y):
            for j in range(self.map_x):
                if self.map[i][j] == -1:
                    self.map[i][j] = choice([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ','+','+',
                                             'G', 'O', 'o', 'T', 'D'])
        self.map[self.boss_y][self.boss_x] = ('B')
        
        

    def check_field(self):
        if self.map[self.player_pos_y][self.player_pos_x] == 'X':
            return 'visited'

        if self.map[self.player_pos_y][self.player_pos_x] == '+':
            return 'heal'

        if self.map[self.player_pos_y][self.player_pos_x] == ' ':
            return 'empty'

        if self.map[self.player_pos_y][self.player_pos_x] == 'G':
            return 'goblin'

        if self.map[self.player_pos_y][self.player_pos_x] == 'D':
            return 'dwarf'

        if self.map[self.player_pos_y][self.player_pos_x] == 'T':
            return 'troll'

        if self.map[self.player_pos_y][self.player_pos_x] == 'o':
            return 'ork'

        if self.map[self.player_pos_y][self.player_pos_x] == 'O':
            return 'ork_general'

        if self.map[self.player_pos_y][self.player_pos_x] == 'B':
            return 'dragon'

    def move_north(self):
        if self.player_pos_y != 0:
            self.map[int(self.player_pos_y)][int(self.player_pos_x)] = 'X'
            self.player_pos_y -= 1
            return 'You walked north!\n', True
        else:
            return 'There is a thick jungle full of dangerous animals. Walking through there would certainly kill you!\n', False


    def move_south(self):
        if self.player_pos_y != self.map_y-1:
            self.map[int(self.player_pos_y)][int(self.player_pos_x)] = 'X'
            self.player_pos_y += 1
            return 'You walked south!\n', True
        else:
            return 'There are huge Mountains that you cannot pass!\n', False

    def move_west(self):
        if self.player_pos_x != 0:
            self.map[int(self.player_pos_y)][int(self.player_pos_x)] = 'X'
            self.player_pos_x -= 1
            return 'You walked west!\n', True
        else:
            return 'You see a big ocean. There is certainly no way past this!\n', False

    def move_east(self):
        if self.player_pos_x != self.map_x-1:
            self.map[int(self.player_pos_y)][int(self.player_pos_x)] = 'X'
            self.player_pos_x += 1
            return 'You walked east!\n', True
        else:
            return 'You see a huge cliff. Jumping of it is no option!\n', False
# end MAP #

enemies = ['Goblin','Troll','Ork','Dwarf']

# ######### CHARACTERS ######### #
class Character(GameMap):
    def __init__(self):
        GameMap.__init__(self)                             
        self.max_hp = None
        self.hp = None
        self.mana = None
        self.attack_damage = None
        self.name = None
        self.spells = None
        self.inventory = None
        self.lvl = None
        self.xp = None
        self.action = None
        self.active_effect = None

    def attack(self, attacker, target):    
        self.action = 'attack'
        if target.hp > 0 and target.action != 'defend':
            target.hp -= int(attacker.attack_damage)
        if target.hp > 0 and target.action == 'defend':
            target.hp -= int(attacker.attack_damage)/2

    def defend(self):
        self.action = 'defend'       

    def drop_item(self):
        pass



class Player(Character, GameMap):

    def __init__(self):        
        Character.__init__(self)        
        self.name = 'Player'
        self.lvl = 1
        self.attack_damage = 15
        self.max_hp = 100
        self.max_mp = 50
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.xp = 0
        self.spells = []
        self.inventory = []
        self.weapon = None
        self.gear = {'Head': 'none',
                    'Torso': 'none',
                    'Legs': 'none',
                    'Feet': 'none'}
        self.dmg_bonus = 0
        
    def update_dmg(self):
        self.attack_damage = self.attack_damage + self.dmg_bonus

    def equip(self, item):        
        if item in weaponlist and item in self.inventory and self.weapon == None:
            self.weapon = item
            self.inventory.remove(item)
            self.dmg_bonus = item.dmg_bonus
            self.update_dmg()
            return True
        elif item in spelllist and item in self.inventory and self.spell == None:
            self.spell = item
            self.inventory.remove(item)
            return True
        return False

    def unequip(self, item):
        if self.weapon != None and item == self.weapon:
            self.attack_damage -= self.dmg_bonus
            self.dmg_bonus = 0            
            self.inventory.append(item)            
            self.weapon = None
            
            return True
        else:
            return False

    def use_item(self, item):
        if not item.usable:
                return False, 'not usable'
        if item not in self.inventory:
            return False, 'not available'
        if item in self.inventory:
            item.use(self)
            for i, v in enumerate(self.inventory):
                if v == item:
                    self.inventory.pop(i)
                    return True, 'success'

    def lvl_up(self):
        lvlup = False 
        if self.lvl == 8:
            self.xp = 0       
        if self.xp >= 100 and self.lvl < 2:
            self.lvl = 2            
            self.max_hp += 20
            self.max_mp += 30
            self.mp = self.max_mp
            self.hp = self.max_hp
            if self.xp >= 100:
                self.xp -= 100
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 1.1      
            lvlup = True      
        if self.xp >= 200 and self.lvl < 3:
            self.lvl = 3
            self.max_hp += 40
            self.hp = self.max_hp
            self.max_mp += 60
            self.mp = self.max_mp
            if self.xp >= 200:
                self.xp -= 200
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 1.3 
            lvlup = True              
        if self.xp >= 400 and self.lvl < 4:
            self.lvl = 4            
            self.max_hp += 60
            self.max_mp += 80
            self.mp = self.max_mp
            self.hp = self.max_hp
            if self.xp >= 400:
                self.xp -= 400
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 1.6 
            lvlup = True              
        if self.xp >= 700 and self.lvl < 5:
            self.lvl = 5            
            self.max_hp += 100
            self.hp = self.max_hp
            self.max_mp += 150
            self.mp = self.max_mp
            if self.xp >= 800:
                self.xp -= 800
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 2    
            lvlup = True           
        if self.xp >= 1300 and self.lvl < 6:
            self.lvl = 6            
            self.max_hp += 130
            self.hp = self.max_hp
            self.max_mp += 200
            self.mp = self.max_mp
            if self.xp >= 1600:
                self.xp -= 1600
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 2.5       
            lvlup = True        
        if self.xp >= 2000 and self.lvl < 7:
            self.lvl = 7            
            self.max_hp += 180
            self.max_mp += 250
            self.mp = self.max_mp
            self.hp = self.max_hp
            if self.xp >= 2400:
                self.xp -= 2400       
            else:
                self.xp = 0
            self.attack_damage = self.attack_damage * 2.7 
            lvlup = True      
        if self.xp >= 2800 and self.lvl < 8:
            self.lvl = 8            
            self.max_hp += 200
            self.hp = self.max_hp
            self.max_mp += 300
            self.mp = self.max_mp
            self.xp = 0
            self.attack_damage = self.attack_damage * 3 
            lvlup = True 

        
        
        if lvlup:
            spellfireball.dmg = round(p.lvl*0.6*30)
            if self.lvl == 8:
                return('LVL up!!! You are now on LVL 8 which is the maximum LVL!')
            else:
                return ('LVL up!!! You are now LVL ' + str(self.lvl) + '!')            
        else:
            return False


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.action = None        
        self.xp_bonus = 0

    def showhp(self):
        return self.name, self.hp

class EnemyGoblin(Enemy):
    def __init__(self, p):
        Enemy.__init__(self)        
        self.xp_bonus = 10
        self.name = 'Goblin'
        self.hp = int(p.max_hp)/2
        self.hp = self.hp.__round__(2)        
        self.attack_damage = int(p.hp)/10
        choices = [healthpotion,manapotion,xppotion]
        self.inventory = [choice(choices)]

class EnemyDwarf(Enemy):
    def __init__(self, p):
        Enemy.__init__(self)
        self.xp_bonus = 35
        self.name = 'Dwarf'
        self.hp = int(p.max_hp)/1.5
        self.hp = self.hp.__round__(2)
        self.attack_damage = int(p.hp)/9
        choices = (healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, sword_bronze)
        self.inventory = [choice(choices)]

class EnemyTroll(Enemy):
    def __init__(self, p):
        Enemy.__init__(self)        
        self.xp_bonus = 25
        self.name = 'Troll'
        self.hp = int(p.max_hp)/1.5
        self.hp = self.hp.__round__(2)
        self.attack_damage = int(p.hp)/8
        choices = (healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, sword_bronze)
        self.inventory = [choice(choices)]

class EnemyOrk(Enemy):            
    def __init__(self, p):
        Enemy.__init__(self)        
        self.xp_bonus = 50
        self.name = 'Ork'
        self.hp = int(p.max_hp)/1
        self.hp = self.hp.__round__(2)
        self.attack_damage = int(p.hp)/5
        choices = (healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, sword_bronze, sword_bronze, sword_bronze, sword_steel)
        self.inventory = [choice(choices)]

class EnemyOrkGeneral(Enemy):
    def __init__(self, p):
        Enemy.__init__(self)
        self.xp_bonus = 75
        self.name = 'Ork General'
        self.hp = int(p.max_hp)*1.3
        self.hp = self.hp.__round__(2)
        self.attack_damage = int(p.hp)/3
        choices = (healthpotion, manapotion, xppotion, healthpotion, manapotion, xppotion, sword_bronze, sword_bronze, sword_steel, sword_steel)
        self.inventory = [choice(choices)]

class EnemyDragon(Enemy):
    def __init__(self, p):
        Enemy.__init__(self)
        self.mp = 999999
        self.xp_bonus = 800
        self.name = 'Dragon'
        self.hp = 2000
        self.inventory = [sword_diamond, manapotion, manapotion, healthpotion]
        self.attack_damage = 30
        self.spell = [spellfireball]
   

# end CHARACTERS #

# ######### ITEMS ######### #
class Item:
    def __init__(self):
        self.name = None
        self.worth = 0
        self.usable = False
        self.equippable = False
        self.weight = 0


class Potion(Item):
    def __init__(self):
        Item.__init__(self)
        self.weight = 0.5
        self.usable = True

class PotionHP(Potion):
    def __init__(self):
        Potion.__init__(self)
        self.name = 'HP Potion'
        self.hp_bonus = 50
        
    def use(self, p):
        p.hp = p.hp + self.hp_bonus
        if p.hp >= p.max_hp:
            p.hp = p.max_hp
        return self.hp_bonus


class PotionXP(Potion):
    def __init__(self):
        Potion.__init__(self)
        self.name = 'XP Potion'
        self.xp_bonus = 150


    def use(self, p):
        p.xp = p.xp + self.xp_bonus
        p.lvl_up
        return self.xp_bonus


class PotionMP(Potion):
    def __init__(self):
        Potion.__init__(self)
        self.name = 'MP Potion'
        self.mp_bonus = 50

    def use(self, p):
        p.mp = p.mp + self.mp_bonus
        if p.mp >= p.max_mp:
            p.mp = p.max_mp
        return self.mp_bonus


class Weapon(Item):
    def __init__(self):
        Item.__init__(self)
        self.dmg_bonus = None
        self.usable = False
        self.equippable = True

class WeaponBronzeSword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = 'Bronze Sword'
        self.dmg_bonus = 10

class WeaponSteelSword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = 'Steel Sword'
        self.dmg_bonus = 40

class WeaponDiamondSword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name = 'Diamond Sword'
        self.dmg_bonus = 160

class Armor(Item):
    pass
# end ITEMS #


# ######### SPELLS ######### #
class Spell():
    def __init__(self): 
        self.name = None       
        self.effect = None
        self.dmg = None
        self.mana_usage = None
        self.effect_dmg = None

    def cast(self, attacker, target):
        target.hp -= self.dmg
        attacker.mp -= self.mana_usage
        target.active_effect = self.effect
        return self.dmg, self.mana_usage, self.effect


class SpellFireball(Spell):
    def __init__(self):        
        Spell.__init__(self)
        self.name = 'Fireball'
        self.dmg = 30
        self.mana_usage = p.lvl*20/0.8
        self.effect_dmg = 5
        self.effect = 'fire'

         
class SpellBlizzard(Spell):
    def __init__(self):
        Spell.__init__(self)
        self.name = 'Blizzard'
        self.dmg = p.lvl*50
        self.mana_usage = p.lvl*30/p.lvl
        self.effect_dmg = 0
        self.effect = 'ice'
# end SPELLS #


# ######### Objects ######### #
p = Player()
e = Enemy()
healthpotion = PotionHP()
manapotion = PotionMP()
xppotion = PotionXP()
spellfireball = SpellFireball()
spellblizzard = SpellBlizzard()
sword_bronze = WeaponBronzeSword()
sword_steel = WeaponSteelSword()
sword_diamond = WeaponDiamondSword()

# ######### ITEMLISTS + SPELLLIST ######### #
weaponlist = [sword_bronze, sword_steel, sword_diamond]
potionlist = [healthpotion, manapotion, xppotion]
spelllist = [spellfireball, spellblizzard]
# end ITEMLISTS + SPELLLIST #
# end OBJECTS #

p.spells.append(spellfireball)
p.inventory.append(sword_bronze)