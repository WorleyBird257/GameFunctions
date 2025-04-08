'''Opens the Adventure Game. Draws from functions in gameFunctions module.
Includes combat loop. updated some functions into purchaseMenuLoop.
 '''

import gameFunctions, random, gameCombatLoop, gamePurchaseMenu, gameUserInventory

user_HP = 50 #still being used for combat code instead of player stat dictionary
GP = 100
startingMoney = GP

player_stats = {'attack': 10, 'defense': 5, 'health': 50, 'equipment': {}}


def town_splash(): 
    '''
    Small 'splash' intro to the game!
    Can be expanded for character creation, new game or loading old one.

    Parameters:
        User input name
        print_welcome function.
        
    Returns:
        None
    '''
    
    print('You are in town.')
    print(f'Current HP: {user_HP}, Current Gold: {GP}')
    print('\nWhat would you like to do?\n')

def get_valid_input():
    '''
    Validates users input to ensure the game's menu only operates with particular text.
    '''
    first_prompt = True
    while True:
        if first_prompt:
            user_input = input("\nSelect a number (1-5): \n").strip()
            first_prompt = False
        else:
            user_input = input("That selection is invalid. Try again (1-5): \n").strip()
        if user_input.isnumeric():
            user_input = int(user_input)
            if 1 <= user_input <= 5:
                return user_input
        print("Invalid selection. Please choose a number between 1 and 5.\n")

def openGameMenu():
    '''
    Main loop for game interaction. Runs one of five branches based on user input.
    '''
    while True:
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
            gameCombatLoop.fightMonster()
        elif action == 2: #shop
            print('You head towards the center of town looking for supplies.')
            gamePurchaseMenu.gameShopLoop(startingMoney)
        elif action == 3: #check inventory
            gameUserInventory.checkInventory()
        elif action == 4: #rest
            print("\nYou find your way to the neighboring inn.\nFor 5 GP you get a hot meal and a bed to sleep in.")
            print('...')
            print("You feel refreshed and ready for your next adventure.")
        elif action == 5: #quit
            print("\nGoodbye, adventurer! See you next time.")
            break
        
if __name__ == '__main__':
    
   # name = input('What is your name?\n') 
   # print(f'\n{gameFunctions.print_welcome(name)}\n')
   # town_splash()
    openGameMenu()
    

