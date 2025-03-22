'''Opens the Adventure Game. Draws from functions in gameFunctions module.
Includes combat loop. '''

import gameFunctions, random, gameCombatLoop

user_HP = 50
GP = 30

def town_splash(): 
    '''
    Small 'splash' intro to the game!

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
            user_input = input("\nSelect a number (1-3): \n").strip()
            first_prompt = False
        else:
            user_input = input("That selection is invalid. Try again (1-3): \n").strip()
        if user_input.isnumeric():
            user_input = int(user_input)
            if 1 <= user_input <= 3:
                return user_input
        print("Invalid selection. Please choose a number between 1 and 3.\n")

def openGameMenu():
    '''
    Main loop for game interaction. Runs one of three branches based on user input.
    '''
    while True:
        print('1) Leave town (Fight monster)')
        print('2) Find a nearby Inn (Restore HP for 5 GP)')
        print('3) Quit')
        
        action = get_valid_input()

        if action == 1:
            print('You leave the town gates and head towards the forest.')
            print('...')
            print('A branch snaps near by!')
            gameCombatLoop.fightMonster()
        elif action == 2:
            print("\nYou find your way to the neighboring inn.\nFor 5 GP you get a hot meal and a bed to sleep in.")
            print('...')
            print("You feel refreshed and ready for your next adventure.")
        elif action == 3:
            print("\nGoodbye, adventurer! See you next time.")
            break
        
if __name__ == '__main__':
    
    name = input('What is your name?\n') 
    print(f'\n{gameFunctions.print_welcome(name)}\n')
    town_splash()
    openGameMenu()
    

