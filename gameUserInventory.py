'''Inventory for game character that can be called for different functions.
Functions for checking, adding, removing items included.
Additional functionality for managing inventory.
'''
from gameData import shop_item_descriptions, healing_amount, item_combat_stats


def item_menu(item, player_instance):
    print(f'What would you like to do with {item}?')
    print('1) Equip Item')
    print('2) Use Item')
    print('3) Discard Item')
    print('4) Return to Inventory')
    
    action = input('Choose an option (1-4): ').strip()
    while action not in ['1', '2', '3', '4']:
        action = input('Invalid choice').strip()
    
    if action == '1':  # Equip item
        player_instance.equip_item(item)
    elif action == '2':  # Use item
        player_instance.heal(item)
    elif action == '3':  # Discard item
        quantity = int(input(f"How many {item}(s) would you like to discard? "))
        player_instance.remove_from_inventory(item, quantity)
    elif action == '4':  # Return
        print('Returning to inventory...\n')
        
def check_inventory(player_instance):
    print('\nYour Inventory:')
    if player_instance.inventory:  # Check if inventory is not empty
        for item, quantity in player_instance.inventory.items():
            print(f'{item}: {quantity}')
        selected_item = input("Select an item. Type 'exit' to quit.\n ").strip().title()

        if selected_item.lower() == 'exit':  # Option to exit the inventory check
            return
        if selected_item in player_instance.inventory:
            #print(f'{shop_item_descriptions[item][]}')
            item_menu(selected_item, player_instance)  # Calls a function to handle item actions
        else:
            print("That item is not in your inventory.")
    else:
        print("There's nothing in there.\n")

def add_to_inventory(item, quantity, player_instance):  # Add items to inventory
    player_instance.add_to_inventory(item, quantity)

def use_item(item, player_instance): # Use item in inventory (healing)
    player_instance.heal()
    
def remove_from_inventory(item, quantity, player_instance):  # Remove items from inventory
    player_instance.remove_from_inventory(item, quantity) 
