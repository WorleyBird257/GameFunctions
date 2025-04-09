'''Opens the Adventure Game.
Updated: 4/9/25
Draws data from gameData to resolve module dependencies.
Able to save game!
Includes:
combatLoop with usable items for combat and healing and random monster generation.
    -items can only be equipped outside of combat. hidden durability stat not implemented.
purchaseMenuLoop: working shop with dynamic inventory - doesn't update after purchase
userInventory: supports combat and non-combat item manipulation
    -unequip function needs better implementing
 '''

import random, gameCombatLoop, gamePurchaseMenu, gameUserInventory
from gameData import player_stats
import json

def save_game(filename, player_stats):
    try:
        with open(filename, 'w') as save_file:
            json.dump(player_stats, save_file)
            print(f"Game successfully saved to {filename}!")
    except IOError:
        print("Error saving the game. Please try again.")
    
def load_game(filename):
    try:
        with open(filename, 'r') as save_file:
            game_data = json.load(save_file)  # Load saved data
        print(f"Game successfully loaded from {filename}!")
        
        # Ensure `gold` is numeric and not None
        game_data['gold'] = game_data.get('gold', 0) or 0  # Reset to 0 if None or invalid
        
        # Similarly, validate other keys as needed
        if game_data.get('max_health') is None:
            game_data['max_health'] = game_data.get('health', 50)  # Default max_health
        
        return game_data  # Return the cleaned data
    except FileNotFoundError:
        print(f"No save file named {filename} found. Starting a new game.")
        return {
            'name': 'Adventurer',
            'attack': 10,
            'defense': 5,
            'health': 50,
            'gold': 100,
            'experience': 0,
            'inventory': {},
            'equipment': {},
        }
    except json.JSONDecodeError:
        print("Error loading the save file—it might be corrupted.")
        return {
            'name': 'Adventurer',
            'attack': 10,
            'defense': 5,
            'health': 50,
            'gold': 100,
            'experience': 0,
            'inventory': {},
            'equipment': {},
        }
        
def start_game(player_stats):
    print("Welcome to the Adventure game!")
    print("1) Start a new game")
    print("2) Load a saved game")
    choice = input("Choose an option (1-2): ").strip()
    
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please select 1 or 2: ").strip()
    
    if choice == '1': #new game
        print('Starting new game...')
        name = input('What is your name?\n')
        player_stats.update({
            'name': name if name else 'Adventurer',
            'attack': 10,
            'defense': 5,
            'health': 50,
            'gold': 100,
            'experience': 0,
            'inventory': {},
            'equipment': {},
            })

        town_splash()

    elif choice == '2':  # Load game 
        filename = input("Enter the filename of your save file: ").strip()

        loaded_data = load_game(filename)
        player_stats.update(loaded_data)
        
         # Ensure player_stats reflects the loaded data
        town_splash()
    return player_stats

def town_splash(): 
    '''
    Small 'splash' intro to the game!
    Can be expanded for character creation, new game or loading old one.

    Parameters:
        User input name
        prints a welcome banner.
        
    Returns:
        None
    '''
    print(f'\nWelcome, {player_stats['name']}!')
    print('You are in town.')
    print(f'Current HP: {player_stats['health']}, Current Gold: {player_stats['gold']}')
    print('\nWhat would you like to do?\n')

def get_valid_input():
    '''
    Validates users input to ensure the game's menu only operates with particular text.
    '''
    first_prompt = True
    while True:
        if first_prompt:
            user_input = input("\nSelect a number (1-5): ").strip()
            first_prompt = False
        else:
            user_input = input("That selection is invalid. Try again (1-5): ").strip()
        if user_input.isnumeric():
            user_input = int(user_input)
            if 1 <= user_input <= 5:
                return user_input
        print("Invalid selection. Please choose a number between 1 and 5. ")

def openGameMenu(player_stats):
    '''
    Main loop for game interaction. Runs one of five branches based on user input.
    '''
    while True:
        print(f'\nCurrent HP: {player_stats['health']}, Current Gold: {player_stats['gold']}')
        print('1) Leave town (Fight monster)')
        print('2) Visit the local market')
        print('3) Check Inventory')
        print('4) Find a nearby Inn (Restore HP for 5 GP)')
        print('5) Quit')
        
        action = get_valid_input()

        if action == 1: #fight
            print('You leave the town gates and head towards the forest.')
            print('...')
            print('A branch snaps near by!')
            gameCombatLoop.fightMonster(player_stats)
            
        elif action == 2: #shop
            print('You head towards the center of town. Markets line the square')
            gamePurchaseMenu.gameShopLoop(player_stats)
            
        elif action == 3: #check inventory
            gameUserInventory.checkInventory()
            
        elif action == 4: #rest
            if player_stats.get('gold', 0) >= 5: #ISSUE
                print("\nYou find your way to the neighboring inn.\nFor 5 GP you get a hot meal and a bed to sleep in.")
                print('...')
                player_stats['health'] = 50  # Restore health to maximum
                player_stats['gold'] -= 5  # Subtract 5 gold from purse
                print("You feel refreshed and ready for your next adventure.")
            else:
                print('The innkeeper shakes their head and points to the stables.')
                player_stats['health'] = max(player_stats['health'] - 5, 0)  # Reduce health but ensure it doesn’t go negative
                print('You find a clean pile of straw to lay down on...')
                print('The roosters wake you up at dawn.\n')
                
        elif action == 5: #quit
            filename = input("Enter a filename to save your game: ").strip()
            save_game(filename, player_stats)
            print("\nGoodbye, adventurer! See you next time.")
            break
    
if __name__ == '__main__':
    
    player_stats = start_game(player_stats)  # Pass player_stats, capture updates
    openGameMenu(player_stats) #open game menu
