'''
Module for game's combat. Wanted seperated from the rest of the the game's functions for clarity. 
Three Functions:
    displayFightStatistics: Shows character and monster's health through out the fight.
    getUserFightOptions: 
'''
import gameFunctions, random, gameUserInventory
from gameData import shop_item_descriptions, healing_amount, item_combat_stats, inventory

def combatItemMenu(item, user_HP):
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
        user_HP = useItemInCombat(item, user_HP)  # Update user_HP
        return user_HP
    elif action == '3':  # Return
        return user_HP  # Return updated user_HP
    return user_HP  # Ensure updated HP is returned
    

def useItemInCombat(item, user_HP):
    if item in inventory and inventory[item] > 0:
        if shop_item_descriptions[item][1] == 'Consumable':
            print(f"You used {item}.")
            gameUserInventory.removeFromInventory(item, 1)  # Reduce quantity in inventory

            if item in healing_amount:
                user_HP += healing_amount[item]
                user_HP = min(user_HP, 50)  # Cap HP at maximum
                print(f"Your HP is now {user_HP}.")
            else:
                print(f"{item} cannot be used in combat.")
        else:
            print(f"{item} cannot be used in combat.")
    else:
        print(f"You don't have any {item}(s) to use.")
    return user_HP

def displayFightStatistics(user_HP, monster): # Displays user and monster HP at start of fight. 
    print(f"Your HP: {user_HP}")
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

def fightMonster(): # Function initiates the combat loop and takes generated monster and user input to run. 
    user_HP = 50 
    monster = gameFunctions.new_random_monster() # Generates a random monster from gameFunctions
    print(f'A wild {monster['name']} appears!\n')

    while monster['health'] > 0 and user_HP > 0: 

        displayFightStatistics(user_HP, monster) # Display health
        action = getUserFightOptions() # Determines user's choice from input
        
        if action == 1: # Attack option
            # User attacks monster (action 1)
            damage_to_monster = random.randint(10, 20)
            monster['health'] -= damage_to_monster
            print(f"\nYou deal {damage_to_monster} damage to the {monster['name']}!")
            
            if monster['health'] <= 0: #Terminating script for when user defeate monster
                print(f"\nYou defeated the {monster['name']}!")
                print(f"You loot {monster['money']} gold coins!")
                break
            
            # Monster attacks user (action 2)
            damage_to_user = random.randint(monster['power'] - 5, monster['power']) 
            user_HP -= damage_to_user
            print(f"The {monster['name']} attacks you for {damage_to_user} damage!")
            
            if user_HP <= 0: #If the monster defeats user, the loop terminates. 
                print("\nYou have been defeated! Better luck next time.")
                break
        elif action == 2:  # Use an Item
            if inventory:  # Check if inventory is not empty
                for item, quantity in inventory.items():
                    print(f"{item}: {quantity}")
                item_to_use = input("Choose an item to use: ").strip().title()
        
                if item_to_use in inventory:
                    user_HP = useItemInCombat(item_to_use, user_HP)  # Update health after item usage
                    # Feedback and transition
            else:
                print(f"{item_to_use} is not in your inventory. Returning to combat...")
            #item_to_use = input("Choose an item to use: ").strip().title()  # Let the player choose an item
            #combatItemMenu(item_to_use)  # Call the combat item menu for actions like equip/use/discard
        elif action == 3: # Flee option
            print(f"\nYou ran away from the {monster['name']}.")
            break

    print("\nExhausted, you return to town...")
