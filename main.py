from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, BooleanProperty
from classes import *

p.randomize_map()
p.position_update()
 

class MainWindow(BoxLayout):        
    p.map_to_string()
    text_map = StringProperty(p.map_string)
    text_textfield = StringProperty('')    
    text_stats = StringProperty('')
    explore_buttons_active = BooleanProperty(True)
    fight_buttons_active = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.field = 'empty'
        self.mode = 'explore'
        self.map_y = p.map_y
        self.map_x = p.map_x
        self.textfield_counter = 0
        self.update_stats()
      
    def update_stats(self):
        text = str(f"STATS:\nHP: {p.hp}/{p.max_hp}\n"
                           f"MP: {p.mp}/{p.max_mp}\n"
                           f"DMG: {p.attack_damage}\n"
                           f"XP: {p.xp}\n"
                           f"LVL: {p.lvl}\n")
        self.text_stats = text
        
    def update_map(self):
        global e

        self.update_stats()
        self.textfield_counter += 1              
        p.map_to_string()
        self.field = p.check_field()
        p.position_update()
        self.text_map = p.map_string  

        enemies = ('dwarf','goblin','ork','ork_general','troll','dragon')
        
        if self.field == 'visited':
            self.text_textfield += 'This place seems familiar...\n'

        elif self.field == 'empty':
            self.text_textfield += 'There is nothing special here...\n'

        elif self.field == 'heal':
            text_heal = 'You feel much better now and also found a healthpotion!\n'
            self.mode == 'explore'            
            self.text_textfield += text_heal
            p.hp = p.max_hp
            p.inventory.append(healthpotion)
            self.update_stats()

        elif self.field in enemies:                        
            if self.field == 'dwarf':
                text_dwarf = 'You see a Dwarf fetching his axe while walking towards you... He jumps towards you and attacks!\n'
                self.text_textfield = text_dwarf
                e = EnemyDwarf(p)

            elif self.field == 'goblin':
                text_goblin = ('You see a Goblin crawling out of a hole on the ground. '
                        'He watches you for a few seconds and then starts to attack you!\n')
                self.text_textfield = text_goblin
                e = EnemyGoblin(p)

            elif self.field == 'ork':
                text_ork = 'You see a Ork agressively walking towards you... He immediately attacks you!\n'
                self.text_textfield = text_ork
                e = EnemyOrk(p)

            elif self.field == 'ork_general':
                text_ork_general = 'You see a Ork agressively walking towards you. It kinda looks fancy... It immediately attacks you!\n'
                self.text_textfield = text_ork_general
                e = EnemyOrkGeneral(p)

            elif self.field == 'troll':
                text_troll = 'You see a Troll stomping on the ground... It spotted you and looks like it wants to fight!\n'
                self.text_textfield = text_troll
                e = EnemyTroll(p)

            elif self.field == 'dragon':
                text_dragon = 'A huge Dragon appears in front of you! This will be a hard fight!\n'
                self.text_textfield = text_dragon
                e = EnemyDragon(p)

            self.mode = 'fight'
            self.text_textfield += 'The fight begins! What do you want to do?\n'
        else:
            self.mode = 'explore'

        if self.mode == 'explore':
            p.map_to_string()
            self.text_map = p.map_string
            self.explore_buttons_active = True
            self.fight_buttons_active = False

        elif self.mode == 'fight':
            choices_begin = ('player', 'enemy')
            begin = choice(choices_begin)
            if begin == 'enemy':
                self.update_fight()
            else:
                text_enemy_hp = str(e.name)+' HP: '+str(e.hp)+' \n'
                self.text_map = text_enemy_hp
            self.explore_buttons_active = False
            self.fight_buttons_active = True

        p.position_update()
        if self.textfield_counter == 11:
            self.text_textfield = ''
            self.textfield_counter = 0  
   
    def update_fight(self):
        self.update_stats()                
        text_enemy_hp = str(e.name)+' HP: '+str(e.hp)+' \n'
        self.text_map = text_enemy_hp
        if self.textfield_counter == 11:
            self.text_textfield = ''
            self.textfield_counter = 0  
        self.enemy_turn()
        if e.hp <= 0:
            text_fightwin = 'You killed the '+e.name+' and got '+str(e.xp_bonus)+'XP!\nLoot Recieved:\n'
            for i in e.inventory:
                p.inventory.append(i)
            for i in e.inventory:
                text_fightwin += i.name+'\n'
            self.text_textfield += text_fightwin
            p.xp = p.xp + e.xp_bonus            
            p.position_update()
            self.mode = 'explore'
            self.update_map()

    def enemy_turn(self):
        move_choices = ('attack', 'defend')
        move = choice(move_choices)
        
        if move == 'defend':
            e.defend()
            self.text_textfield += 'The '+e.name+' defends!\n'
            self.textfield_counter += 1
        if move == 'attack':
            e.attack(e,p)
            self.text_textfield += 'The '+e.name+' attacks you for '+str(e.attack_damage)+'DMG!\n'
            self.textfield_counter += 1

    def go_north(self):        
        p.move_north()
        self.update_map() 
  
    def go_south(self):       
        p.move_south()
        self.update_map()
  
    def go_west(self):               
        p.move_west()
        self.update_map()
  
    def go_east(self):             
        p.move_east()
        self.update_map()
  
    def attack(self):
        text = 'You attacked the '+str(e.name)+' for '+str(p.attack_damage)+'DMG!\n'
        self.text_textfield += text
        self.textfield_counter += 1
        self.update_fight()
        p.attack(p,e)
  
    def defend(self):
        self.text_textfield += 'You defend!\n'
        p.defend()

    def cast_spell(self):
        pass

    def run_away(self):
        pass

    def equip(self):
        pass
    
    def unequip(self):
        pass

    def use(self):
        pass


class TextRPG_kivygui(App):
    pass

if __name__ == '__main__':
    TextRPG_kivygui().run()