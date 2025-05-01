'''
Module for game's combat. Wanted seperated from the rest of the the game's functions for clarity. 
Functions:
    displayFightStatistics: Shows character and monster's health through out the fight.
    getUserFightOptions:
    fightMonster: loop for combat. allows for item use with combatItemMenu and useItemInCombat
    combatItemMenu: menu allows manipulating items while in combat
    useItemInCombat: properly handles item use

    random_stat: produces a random integer at x,y range for generating monster stats
    new_random_monster: produces a monster to fight. 
'''
import random, gameUserInventory, game
from wanderingMonster import WanderingMonster
from gameData import shop_item_descriptions, healing_amount, item_combat_stats, Player
from gameData import tileSize, MapHeight, MapWidth, SCREEN_WIDTH, SCREEN_HEIGHT, colors, town_x, town_y

def fight_monster(player_instance, monster): 
    print(f"A wild {monster.name} appears!\n")
 
    while  monster.health > 0 and player_instance.health > 0: 
        display_fight_statistics(player_instance, monster)  # Display health
        action = get_user_fight_options()  # Get user's choice

        if action == 1:  # Attack option
            # player_instance attacks monster
            equipped_weapon = player_instance.equipment.get('hand')  # checks weapon stat
            item_attack_stat = item_combat_stats.get(equipped_weapon, [0])[0] if equipped_weapon else 0  # Fetch attack stats for equipped item
            damage_to_monster = random.randint(10, 20) + item_attack_stat
            monster.health -= damage_to_monster
            print(f"\nYou deal {damage_to_monster} damage to the {monster.name}!")
            
            # Check if monster is defeated
            if  monster.health <= 0:
                player_instance.gold += monster.gold
                player_instance.experience += monster.experience
                print(f"\nYou defeated the {monster.name}!")
                print(f"You loot {monster.gold} gold coins!")
                print(f"You gain {monster.experience} experience!")
                break
            
            # Monster attacks user
            equipped_shield = player_instance.equipment.get('off hand')  # check shield stat
            item_defense_stat = item_combat_stats.get(equipped_shield, [1])[0] if equipped_shield else 0 # Fetch defense stats for equipped item
            damage_to_user = (random.randint(monster.power - 5, monster.power)) - (player_instance.defense + item_defense_stat)
            if damage_to_user <= 0: #prevents monster from dealing negative damage
                damage_to_user = 0
            player_instance.health -= damage_to_user
            print(f"The {monster.name} attacks you for {damage_to_user} damage!")

            # Check if the Player is defeated
            if player_instance.health <= 0:
                print("\nYou have been defeated!")
                print('Bloody and weary, you return to town.')
                player_instance.position = (4,5)
                break
                
        elif action == 2:  # Use an Item
            item_to_use = None
            if player_instance.inventory:  # Check if inventory is not empty
                print("Inventory:")
                for item, quantity in player_instance.inventory.items():
                    print(f"{item}: {quantity}")
                item_to_use = input("Choose an item to use: ").strip().title()

                if item_to_use in player_instance.inventory:
                    if item_to_use == "Bomb":  # Bomb exception logic
                        monster.health = 0  # OHKO the monster
                        player_instance.gold += monster.gold
                        player_instance.experience += monster.experience
                        player_instance.remove_from_inventory(item_to_use, 1)
                        print(f"You used {item_to_use}. The {monster.name} is obliterated!")
                        print(f'Only a crater remains.')
                        break
                    else:
                        player_instance.heal(item_to_use) # use item for healing
                else:
                    print('That item is not found in your inventory.')

                # Check if the item quantity reaches 0
                if player_instance.inventory.get(item_to_use, 0) == 0:
                    print(f"You have no more {item_to_use}s left.")
                continue
                
        elif action == 3:  # Flee option #avoids infinite monster loop
            print(f"\nYou ran away from the {monster.name}.")
            player_instance.move('down')
            break
    
def display_fight_statistics(player_instance, monster): # Displays user and monster HP at start of fight.
    print(f"Your HP: {player_instance.health}")
    print(f"{monster.name} HP: { monster.health}")

def get_user_fight_options(): # Combat menu with three options. Validates input within function.
    print('\nWhat would you like to do?')
    print('1) Attack')
    print('2) Item')
    print('3) Run away')
    choice = input('Choose an option (1 - 3): ').strip()
    while choice not in ['1', '2', '3']:
        choice = input("Invalid choice. Please select 1, 2 or 3: ").strip()
    return int(choice)

def combat_item_menu(item, player_instance):
    print(f"\nWhat would you like to do with {item}?")
    print("1) Equip Item")
    print("2) Use Item")
    print("3) Return")

    action = input("Choose an option (1-3): ").strip()
    while action not in ['1', '2', '3']:
        action = input("Invalid choice. Please select 1, 2, or 3: ").strip()

    if action == '1':  # Equip Item
        player_instance.equipItem(item)
        
    elif action == '2':  # Use Item
        player_instance.heal(item) # Update Player health
        
    elif action == '3':  # Return
        print('Returning to combat')
    
    return player_instance.health  # Ensure updated HP is returned
