'''Opens the Adventure Game.
Updated: 4/30/25
Draws data from gameData to resolve module dependencies.
Able to save game!
There's graphics and monsters that move!

Includes:
combatLoop with usable items for combat and healing and random monster generation.
    -items can only be equipped outside of combat. hidden durability stat not implemented.
purchaseMenuLoop: working shop with dynamic inventory - doesn't update after purchase
userInventory: supports combat and non-combat item manipulation
    -unequip function needs better implementing
 '''
import json
import gameCombatLoop
import gamePurchaseMenu
import gameUserInventory
import gameExplore
from gameData import game_map, tileSize, MapHeight, MapWidth, SCREEN_WIDTH, SCREEN_HEIGHT, colors, town_x, town_y, Player
from wanderingMonster import WanderingMonster  

def openGameMenu(player_instance, game_map):
    '''
    Main loop for game interaction. Runs one of five branches based on user input.
    '''
    while True:
        print(f'\nCurrent HP: {player_instance.health}, Current Gold: {player_instance.gold}')
        print('1) Leave town ')
        print('2) Visit the local market')
        print('3) Check Inventory')
        print('4) Find a nearby Inn (Restore HP for 5 GP)')
        print('5) Quit')
        
        action = get_valid_input()

        if action == 1: #fight / explore
            print('You leave the town gates and head towards the forest...')
            player_instance_x, player_instance_y = player_instance.position
            player_move_counter = 0
            # Ensure monsters are initialized
            monsters = WanderingMonster.generate_initial_monsters()
            gameExplore.explore_map(player_instance, monsters, player_move_counter=0)  # Pass monsters into the function
            
        elif action == 2: #shop
            print('You head towards the center of town. Markets line the square')
            gamePurchaseMenu.game_shop_loop(player_instance)
            
        elif action == 3: #check inventory
            gameUserInventory.check_inventory(player_instance)
            
        elif action == 4: #rest
            if player_instance.gold >= 5: 
                print("\nYou find your way to the neighboring inn.\nFor 5 GP you get a hot meal and a bed to sleep in.")
                print('...')
                player_instance.health = 50  # Restore health to maximum
                player_instance.gold -= 5  # Subtract 5 gold from purse
                print("You feel refreshed and ready for your next adventure.")
            else:
                print('The innkeeper shakes their head and points to the stables.')
                player_instance.health = max(player_instance.health - 5, 0)  # Reduce health but ensure it doesn’t go negative
                print('You find a clean pile of straw to lay down on...')
                print('The roosters wake you up at dawn.\n')
                
        elif action == 5: #quit
            filename = input("Enter a filename to save your game: ").strip()
            save_game(filename, player_instance, game_map)
            print("\nGoodbye, adventurer! See you next time.")
            break

def town_splash(player_instance): 
    '''
    Small 'splash' intro to the game!
    Can be expanded for character creation, new game or loading old one.

    Parameters:
        User input name
        prints a welcome banner.
        
    Returns:
        None
    '''
    print(f'\nWelcome, {player_instance.name}!')
    print('You are in town.')
    print(f"Current HP: {player_instance.health}, Current Gold: {player_instance.gold}")
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

def start_game():
    print("Welcome to the Adventure game!")
    print("1) Start a new game")
    print("2) Load a saved game")
    choice = input("Choose an option (1-2): ").strip()

    # Validate user choice
    while choice not in ['1', '2']:
        choice = input("Invalid choice. Please select 1 or 2: ").strip()

    if choice == '1':  # New game
        print('Starting new game...')
        name = input('What is your name?\n')
        player_instance = Player(
            name=name if name else 'Adventurer',  # Default to 'Adventurer'
            health=50,
            gold=100,
            position=(4, 5)
        )
        game_map = [[0] * MapWidth for _ in range(MapHeight)]  # Dynamic map size
        town_splash(player_instance)
        return player_instance, game_map

    elif choice == '2':  # Load saved game
        filename = input("Enter the save file name (default: save_game.json): ").strip()
        if not filename:  # Provide a default file name if none is given
            filename = "save_game.json"
        try:
            player_instance, game_map = load_game(filename)
            return player_instance, game_map
        
        except Exception as e:
            print(f"Failed to load save file: {e}")
            print("Starting a new game instead...")
            player_instance = Player(name="Adventurer", health=50, gold=100, position=(4, 5))
            game_map = [[0] * MapWidth for _ in range(MapHeight)]
            return player_instance, game_map

    # Fallback in case of invalid choice (shouldn't trigger with proper logic)
    else:
        print("Invalid option, starting a default new game...")
        player_instance = Player(name="Adventurer", health=50, gold=100, position=(4, 5))
        game_map = [[0] * MapWidth for _ in range(MapHeight)]

def save_game(filename, player_instance, game_map):
    """Save the player's progress and game state to a file."""
    try:
        save_data = {
            "player": player_instance.to_dict(),
            "game_map": game_map,
        }
        with open(filename, "w") as save_file:
            json.dump(save_data, save_file, indent=4)
        print(f"Game saved successfully to {filename}!")
    except Exception as e:
        print(f"An error occurred while saving the game: {e}")
        
def load_game(filename):
    """Load the player's progress and game state from a file."""
    try:
        with open(filename, "r") as save_file:
            save_data = json.load(save_file)

        # Reconstruct the Player instance
        player_instance = Player.from_dict(save_data["player"])

        # Retrieve the game map
        game_map = save_data["game_map"]

        print("Game loaded successfully!")
        return player_instance, game_map
    except FileNotFoundError:
        print("Save file not found! Starting a new game...")
        return Player(name="Adventurer", health=50, gold=100, position=(4, 5)), [[0] * MapWidth for _ in range(MapHeight)]
    except Exception as e:
        print(f"An error occurred while loading the game: {e}")
        return Player(name="Adventurer", health=50, gold=100, position=(4, 5)), [[0] * MapWidth for _ in range(MapHeight)]

if __name__ == '__main__':
    
    player_instance, game_map = start_game()
    openGameMenu(player_instance, game_map)
