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
import random, gameUserInventory
from gameData import shop_item_descriptions, healing_amount, item_combat_stats, inventory, player_stats

def random_stat(min_val, max_val):
    return random.randint(min_val, max_val)

def new_random_monster(monster_name=None): 
    '''
    Creates a monster with randomized health, power, and money values associated to name and a brief description.

    Parameters:
        monster_name (str)

    Returns:
        monster_values (dict)

    Example:
        >>> new_random_monster('Goblin')
    '''
    
    monster_values_dict = {
        'Goblin': {'health': random_stat(140, 160), 'power': random_stat(15, 30), 'gold': random_stat(1, 10), 'experience': random_stat(15, 30)},
        'Draugr': {'health': random_stat(140, 175), 'power': random_stat(15, 25), 'gold': random_stat(1, 15), 'experience': random_stat(15, 30)},
        'Bat': {'health': random_stat(50, 80), 'power': random_stat(10, 25), 'gold': random_stat(1, 7), 'experience': random_stat(15, 30)},
        'Wolf': {'health': random_stat(150, 180), 'power': random_stat(15, 20), 'gold': random_stat(5, 15), 'experience': random_stat(15, 30)},
        'Skeleton': {'health': random_stat(160, 200), 'power': random_stat(20, 40), 'gold': random_stat(10, 25), 'experience': random_stat(15, 30)}
    }

    monster_description_dict = { #second dictionary holds monster name with description. Ties the two together
        'Goblin': 'Just a greedy little green guy!',
        'Draugr': 'A soulless corpse risen through necromancy',
        'Bat': 'Definitely not a vampire in disguise.',
        'Wolf': 'Lonely and hungry',
        'Skeleton': 'What is dead may never die.'
    }
    
    if monster_name is None: #allows for testing of a monster with different values with same name
        monster_name = random.choice(list(monster_values_dict.keys()))
        
    monster_values = monster_values_dict[monster_name]
        
    return { #outputs dictionary of monster name, description, and (randomized values). feels rough, would rather it output cleaner.
        'name': monster_name,
        'description': monster_description_dict[monster_name],
        'health': monster_values['health'],
        'power': monster_values['power'],
        'gold': monster_values['gold'],
        'experience': monster_values['experience'],
        }

def combatItemMenu(item, player_stats):
    #health = player_stats['health']
    print(f"\nWhat would you like to do with {item}?")
    print("1) Equip Item")
    print("2) Use Item")
    print("3) Return")

    action = input("Choose an option (1-3): ").strip()
    while action not in ['1', '2', '3']:
        action = input("Invalid choice. Please select 1, 2, or 3: ").strip()

    if action == '1':  # Equip Item
        gameUserInventory.equipItem(item)
    elif action == '2':  # Use Item
        player_stats['health'] = useItemInCombat(item, player_stats['health'])  # Update player_stats['health']
        return player_stats['health']
    elif action == '3':  # Return
        return player_stats['health']  # Return updated player_stats['health']
    return player_stats['health']  # Ensure updated HP is returned
    

def useItemInCombat(item, player_stats, monster):
    # Check if the item exists in inventory and is usable
    if item in player_stats['inventory'] and player_stats['inventory'][item] > 0:
        if shop_item_descriptions[item][1] == 'Consumable':
            if item == 'Bomb':  # Special case for "Bomb"
                print(f"You used {item}. The {monster['name']} is obliterated! Nothing remains...")
                player_stats['inventory'][item] -= 1  # Reduce bomb quantity
                monster['health'] = 0  # Instantly defeat the monster
                
                # Grant gold and experience
                player_stats['gold'] += monster['money']
                print(f"You loot {monster['gold']} gold coins!")
                player_stats['experience'] += monster.get('experience', 0)
                print(f"You gain {monster['experience']} experience!")
                return player_stats, monster
            
            elif item in healing_amount:  # Healing item
                player_stats['health'] += healing_amount[item]
                player_stats['health'] = min(player_stats['health'], 50)  # Cap HP at max
                print(f"Your HP is now {player_stats['health']}.")
                player_stats['inventory'][item] -= 1  # Reduce item quantity
        else:
            print(f"{item} is not a usable item.")
    else:
        print(f"You don't have any {item}(s) to use.")
    return player_stats, monster

def displayFightStatistics(player_stats, monster): # Displays user and monster HP at start of fight.
    health = player_stats['health']
    print(f"Your HP: {player_stats['health']}")
    print(f"{monster['name']} HP: {monster['health']}")

def getUserFightOptions(): # Combat menu with two options. Validates input within function.
    print('\nWhat would you like to do?')
    print('1) Attack')
    print('2) Item')
    print('3) Run away')
    choice = input('Choose an option (1 - 3): ').strip()
    while choice not in ['1', '2', '3']:
        choice = input("Invalid choice. Please select 1, 2 or 3: ").strip()
    return int(choice)

def fightMonster(player_stats): 
    monster = new_random_monster()  # Generate a random monster
    print(f'A wild {monster['name']} appears!\n')

    while monster['health'] > 0 and player_stats['health'] > 0: 
        displayFightStatistics(player_stats, monster)  # Display health
        action = getUserFightOptions()  # Get user's choice

        if action == 1:  # Attack option
            # User attacks monster
            equipped_item = player_stats['equipment'].get('hand')  # Replace with your inventory logic
            if equipped_item:  # Ensure there’s something equipped
                item_attack_stat = item_combat_stats.get(equipped_item, [0])[0]  # Fetch attack stats for equipped item
            else:
                item_attack_stat = 0 
            damage_to_monster = random.randint(10, 20) + item_attack_stat
            monster['health'] -= damage_to_monster
            print(f"\nYou deal {damage_to_monster} damage to the {monster['name']}!")
            
            # Check if monster is defeated
            if monster['health'] <= 0:
                # First retrieve the current gold value, modify it, then reassign
                player_stats['gold'] = player_stats.get('gold', 0) + (monster.get('gold') or 0)
                #player_stats.get('gold', 0) += monster.get('money', 0)  # Default to 0
                print(f"\nYou defeated the {monster['name']}!")
                
                print(f"You loot {monster['gold']} gold coins!")
                player_stats['experience'] += monster.get('experience', 0)
                print(f"You gain {monster['experience']} experience!")
                break
            
            # Monster attacks user
            equipped_item = player_stats['equipment'].get('off hand')  # Replace with your inventory logic
            if equipped_item:  # Ensure there’s something equipped
                item_defense_stat = item_combat_stats.get(equipped_item, [0])[0]  # Fetch attack stats for equipped item
            else:
                item_defense_stat = 0
            #item_defense_stat = item_combat_stats.get(equipped_item, [1])[0]
            damage_to_user = (random.randint(monster['power'] - 5, monster['power'])) - (player_stats['defense'] + item_defense_stat)
            if damage_to_user <=0:
                damage_to_user = 0
            player_stats['health'] -= damage_to_user
            print(f"The {monster['name']} attacks you for {damage_to_user} damage!")

            # Check if the player is defeated
            if player_stats['health'] <= 0:
                print("\nYou have been defeated! Better luck next time.")
                break

        elif action == 2:  # Use an Item
            if player_stats['inventory']:  # Check if inventory is not empty
                print("Inventory:")
                for item, quantity in player_stats['inventory'].items():
                    print(f"{item}: {quantity}")
                item_to_use = input("Choose an item to use: ").strip().title()
                if item_to_use in player_stats['inventory']:
                    quantity = player_stats['inventory'][item_to_use]
                    if quantity > 0:
                        print(f"You use {item_to_use}.")

                        player_stats, monster = useItemInCombat(item_to_use, player_stats, monster)  # Update stats
                        if player_stats['inventory'][item_to_use] == 0:
                            print(f'You have no more {item_to_use} left.')
                if monster['health'] <= 0:  # Check if monster is killed by an item
                    break
                #else:
                    #print('That item cannot be found')
            else:
                print("Your inventory is empty. Returning to combat...")
                
        elif action == 3:  # Flee option
            print(f"\nYou ran away from the {monster['name']}.")
            break
    return player_stats
    print("\nExhausted, you return to town...")
