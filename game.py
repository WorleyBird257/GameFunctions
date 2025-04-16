'''Opens the Adventure Game.
Updated: 4/16/25
Draws data from gameData to resolve module dependencies.
Able to save game!
Includes:
combatLoop with usable items for combat and healing and random monster generation.
    -items can only be equipped outside of combat. hidden durability stat not implemented.
purchaseMenuLoop: working shop with dynamic inventory - doesn't update after purchase
userInventory: supports combat and non-combat item manipulation
    -unequip function needs better implementing
 '''
import random, json
import gameCombatLoop, gamePurchaseMenu, gameUserInventory, gameExplore
from gameData import player_stats
from gameData import game_map
from wanderingMonster import WanderingMonster  
#monsters = WanderingMonster.generate_initial_monsters()

def save_game(filename, player_stats, game_map):
    save_data = {
        'player_stats': player_stats,
        'game_map': game_map
        }
    try:
        with open(filename, 'w') as save_file:
            json.dump(save_data, save_file)
            print(f"Game successfully saved to {filename}!")
    except IOError:
        print("Error saving the game. Please try again.")
    
def load_game(filename):
    try:
        with open(filename, 'r') as save_file:
            save_data = json.load(save_file)  # Load saved data
        print(f"Game successfully loaded from {filename}!")

        player_stats = save_data.get('player_stats', {})
        game_map = save_data.get('game_map', [[0] * 10 for _ in range(10)])  # Default empty map if missing

        player_stats['position'] = tuple(player_stats.get('position', (4,5)))
        # Ensure 'gold' is numeric and not None
        player_stats['gold'] = player_stats.get('gold', 0) or 0  # Reset to 0 if None or invalid
        
        # Similarly, validate other keys as needed
        if player_stats.get('max_health') is None:
            player_stats['max_health'] = player_stats.get('health', 50)  # Default max_health
        
        return player_stats, game_map  # Return the cleaned data
    except FileNotFoundError:
        print(f"No save file named {filename} found. Starting a new game.")
        return {
            'name': 'Adventurer',
            'attack': 10,
            'defense': 10,
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
            'defense': 10,
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
            'defense': 10,
            'health': 50,
            'gold': 100,
            'experience': 0,
            'inventory': {},
            'equipment': {},
            'position': (4,5),
            })

        game_map = [[0] * 10 for _ in range(10)]

        town_splash(player_stats)

    elif choice == '2':  # Load game 
        filename = input("Enter the filename of your save file: ").strip()

        player_stats, game_map = load_game(filename)
        #player_stats.update(loaded_data)
        
         # Ensure player_stats reflects the loaded data
        town_splash(player_stats)
        
    return player_stats, game_map

def town_splash(player_stats): 
    '''
    Small 'splash' intro to the game!
    Can be expanded for character creation, new game or loading old one.

    Parameters:
        User input name
        prints a welcome banner.
        
    Returns:
        None
    '''
    print(f'\nWelcome, {player_stats["name"]}!')
    print('You are in town.')
    print(f"Current HP: {player_stats['health']}, Current Gold: {player_stats['gold']}")
    print('\nWhat would you like to do?')

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

def openGameMenu(player_stats, game_map):
    '''
    Main loop for game interaction. Runs one of five branches based on user input.
    '''
    while True:
        print(f'\nCurrent HP: {player_stats['health']}, Current Gold: {player_stats['gold']}')
        print('1) Leave town ')
        print('2) Visit the local market')
        print('3) Check Inventory')
        print('4) Find a nearby Inn (Restore HP for 5 GP)')
        print('5) Quit')
        
        action = get_valid_input()

        if action == 1: #fight / explore
            print('You leave the town gates and head towards the forest...')
            player_x, player_y = player_stats.get('position', (4,5))
            player_move_counter = 0 #********
            # Ensure monsters are initialized
            monsters = WanderingMonster.generate_initial_monsters()
            gameExplore.explore_map(player_x, player_y, player_stats, monsters, player_move_counter)  # Pass monsters into the function
            
        elif action == 2: #shop
            print('You head towards the center of town. Markets line the square')
            gamePurchaseMenu.gameShopLoop(player_stats)
            
        elif action == 3: #check inventory
            gameUserInventory.checkInventory()
            
        elif action == 4: #rest
            if player_stats.get('gold', 0) >= 5: 
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
            save_game(filename, player_stats, game_map)
            print("\nGoodbye, adventurer! See you next time.")
            break
    
if __name__ == '__main__':
    
    player_stats, game_map = start_game(player_stats)
    # print(player_stats)
    # Pass player_stats, capture updates
    openGameMenu(player_stats, game_map) #open game menu
