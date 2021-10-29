from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from classes import *
from kivy.lang import Builder
from kivy.resources import resource_add_path

p.randomize_map()
p.position_update()
p.inventory.append(healthpotion)
p.inventory.append(manapotion)



class MainWindow(BoxLayout):        
    p.map_to_string()
    text_map = StringProperty(p.map_string)
    text_textfield = StringProperty('')    
    text_stats = StringProperty('')
    explore_buttons_active = BooleanProperty(True)
    fight_buttons_active = BooleanProperty(False)
    inventory_items = ListProperty([i.name for i in p.inventory])
    spells_items = ListProperty([i.name for i in p.spells])
    spinner_items_text = StringProperty()
    spinner_spells_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.field = 'empty'
        self.mode = 'explore'
        self.map_y = p.map_y
        self.map_x = p.map_x
        self.textfield_counter = 0
        self.update_stats()
        self.spinner_items_update()
        self.selected_item_str = ''
        self.selected_item_obj = None   
        self.selected_spell_str = ''
        self.selected_spell_obj = None     
        self.spinner_items_text = 'click to select item'
        self.spinner_spells_text = 'click to select spell'

    def spinner_items_clicked(self,value):
        self.spinner_items_text = value
        self.selected_item_str = value
        if self.selected_item_str == 'Diamond Sword':
            self.selected_item_obj = sword_diamond
        elif self.selected_item_str == 'Steel Sword':
            self.selected_item_obj = sword_steel
        elif self.selected_item_str == 'Bronze Sword':
            self.selected_item_obj = sword_bronze
        elif self.selected_item_str == 'HP Potion':
            self.selected_item_obj = healthpotion
        elif self.selected_item_str == 'MP Potion':
            self.selected_item_obj = manapotion
        elif self.selected_item_str == 'XP Potion':
            self.selected_item_obj = xppotion
        print(self.selected_item_obj)
        self.spinner_items_update()

    def spinner_items_update(self):        
        self.inventory_items = [i.name for i in p.inventory]
        self.inventory_items.sort()

    def spinner_spells_clicked(self,value):
        self.spinner_spells_text = value
        self.selected_spell_str = value
        if self.selected_spell_str == 'Fireball':
            self.selected_spell_obj = spellfireball
        elif self.selected_spell_str == 'Blizzard':
            self.selected_spell_obj = spellblizzard

        print(self.selected_spell_obj)
        self.spinner_spells_update()

    def spinner_spells_update(self):        
        self.spells_items = [i.name for i in p.spells]
        self.spells_items.sort()


    def update_stats(self):
        weapon_name = 'None'
        if hasattr(p.weapon, 'name'):
            weapon_name = p.weapon.name
        lvl_check = str(p.lvl_up())
        if lvl_check != 'False':
            self.text_textfield += lvl_check+'\n'
        text = str(f"STATS:\nHP: {p.hp}/{p.max_hp}\n"
                           f"MP: {p.mp}/{p.max_mp}\n"
                           f"DMG: {p.attack_damage}\n"
                           f"XP: {p.xp}\n"
                           f"LVL: {p.lvl}\n"
                           f"Equipped weapon: {weapon_name}\n")
        self.text_stats = text
        
    def update_map(self):
        global e
        self.textfield_counter += 1
        if self.textfield_counter >= 11:
            self.text_textfield = ''
            self.textfield_counter = 0  

        self.update_stats()                      
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
            p.mp = p.max_mp
            p.inventory.append(healthpotion)
            self.spinner_items_update()
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
   
    def update_fight(self):    
        self.textfield_counter += 1    
        if self.textfield_counter >= 11:
            self.text_textfield = ''
            self.textfield_counter = 0 


        self.update_stats()                
        text_enemy_hp = str(e.name)+' HP: '+str(e.hp)+' \n'
        self.text_map = text_enemy_hp
        

        # STATUSEFFECTS
        if e.active_effect == 'fire':
            e.hp -= p.lvl*5
            self.text_textfield += 'The enemy is burning and recieved '+str(p.lvl*5)+' additional DMG!\n'            
        
        if e.hp > 0 and e.active_effect != 'ice':
            self.enemy_turn()

        else:
            self.text_textfield += 'The '+str(e.name)+' is frozen and cant do anything!\n'

        if p.hp <=0:
            self.text_textfield += 'The '+e.name+' killed you!\n GAME OVER!\n'   
            self.text_map = 'YOU ARE DEAD! GAME OVER!'
            self.fight_buttons_active = False
            self.explore_buttons_active = False
            self.ids.button_use_item.disabled = True
            self.ids.spinner_items.disabled = True
            

        if e.hp <= 0:
            if e.name == 'Dragon':
                self.text_textfield = ''
                text_fightwin = 'You defeated the Dragon and won the Game!\nFeel free to explore the rest of the World!\nYou recieved the Blizzard spell!\n\n\nTextRPG Kivy Edition created by:\n Alexander "aTTaX" Müller\n\nLoot recieved:\n'
                p.spells.append(spellblizzard)
            else:
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
            self.spinner_spells_update()
            self.spinner_items_update()

    def enemy_turn(self):
        move_choices = ('attack', 'defend')
        move = choice(move_choices)
        
        if move == 'defend':
            e.defend()
            self.text_textfield += 'The '+e.name+' defends!\n'
            self.textfield_counter += 1
        if move == 'attack':
            e.attack(e,p)
            self.text_textfield += 'The '+e.name+' attacks you for '+str(round(e.attack_damage))+'DMG!\n'
            self.textfield_counter += 1
            self.update_stats()

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
        text = 'You attacked the '+str(e.name)+' for '+str(round(p.attack_damage))+'DMG!\n'
        self.text_textfield += text
        self.textfield_counter += 1
        p.attack(p,e)
        self.update_fight()
          
    def defend(self):
        self.text_textfield += 'You defend!\n'
        p.defend()
        self.update_fight()

    def cast_spell(self):
        if self.selected_spell_obj in p.spells:
            if p.mp >= self.selected_spell_obj.mana_usage:
                self.text_textfield += 'You casted a '+self.selected_spell_obj.name+' this caused '+str(self.selected_spell_obj.dmg)+'DMG and the enemy has now the "'+self.selected_spell_obj.effect+'" statuseffect!\n '
                self.selected_spell_obj.cast(p, e)
                self.update_fight()
            else:
                self.text_textfield += 'You dont have enough MP!\n'
        else:
            self.text_textfield += 'Select a spell first!\n'
  
    def run_away(self):
        choices = (True, False)
        choose = choice(choices)
        if choose: 
            self.text_textfield += 'You successfully ran away!\n'
            self.mode = 'explore'
            self.update_map()
        else:
            self.text_textfield += 'You failed to run away!\n'
            self.update_fight()
            
    def equip(self):  
        self.spinner_items_text = 'click to select item'      
        self.textfield_counter += 1
        if p.equip(self.selected_item_obj):
            self.text_textfield += 'You equipped the '+self.selected_item_obj.name+'!\n'
        else:
            self.text_textfield += 'You cant equip this item!\n'
        self.spinner_items_update()
        self.update_stats()

    def unequip(self):
        weapon_name = 'None'
        if hasattr(p.weapon, 'name'):
            weapon_name = p.weapon.name
        self.textfield_counter += 1
        if p.unequip(p.weapon):
            self.text_textfield += 'You unequipped the '+weapon_name+'!\n'
        else:
            self.text_textfield += 'You cant unequip this item!\n'
        self.spinner_items_update()
        self.update_stats()

    def use_item(self):     
       
        self.spinner_items_text = 'click to select item'
        if self.selected_item_obj in p.inventory and self.selected_item_obj.usable:            
            self.selected_item_obj.use(p)
            p.inventory.remove(self.selected_item_obj)
            if self.selected_item_obj.name == 'HP Potion':
                self.text_textfield += 'You used a HP Potion!\n'
            elif self.selected_item_obj.name == 'MP Potion':
                self.text_textfield += 'You used a MP Potion!\n'
            elif self.selected_item_obj.name == 'XP Potion':
                self.text_textfield += 'You used a XP Potion!\n'            

        elif self.selected_item_obj not in p.inventory:
            self.text_textfield += 'You dont have this item!\n'

        elif not self.selected_item_obj.usable:
            self.text_textfield += 'You cant use this item!\n'
            
        self.selected_item_obj = None

        if self.mode == 'explore':
            self.update_map()
        else: 
            self.update_fight()

        self.spinner_items_update()
        self.update_stats()

       

class TextRPG(App):
    def build(self):
        Builder.load_file('textrpg_kivygui.kv')        
        return MainWindow()
    pass

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    TextRPG().run()