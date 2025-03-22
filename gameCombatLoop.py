'''
Module for game's combat. Wanted seperated from the rest of the the game's functions for clarity. 
Three Functions:
    displayFightStatistics: Shows character and monster's health through out the fight.
    getUserFightOptions: 
'''
import gameFunctions, random

def displayFightStatistics(user_HP, monster): # Displays user and monster HP at start of fight. 
    print(f"Your HP: {user_HP}")
    print(f"{monster['name']} HP: {monster['health']}")

def getUserFightOptions(): # Combat menu with two options. Validates input within function.
    print("\nWhat would you like to do?")
    print("1) Attack")
    print("2) Run away")
    choice = input("Choose an option (1 or 2): ").strip()
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please select 1 or 2: ").strip()
    return int(choice)

def fightMonster(): # Function initiates the combat loop and takes generated monster and user input to run. 
    user_HP = 50 
    monster = gameFunctions.new_random_monster() # Generates a random monster from gameFunctions
    print(f'A wild {monster['name']} appears!\n')

    while monster['health'] > 0 and user_HP > 0: 

        displayFightStatistics(user_HP, monster) # Display combat stats
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
        
        elif action == 2: # Flee option
            print(f"\nYou ran away from the {monster['name']}.")
            break

    print("\nExhausted, you return to town...")
