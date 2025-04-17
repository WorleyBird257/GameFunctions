'''Inventory for game character that can be called for different functions.
Functions for checking, adding, removing items included.
Additional functionality for managing inventory.
'''
from gameData import shop_item_descriptions, healing_amount, item_combat_stats, inventory
from gameData import player_stats

def itemMenu(item):
    print(f'What would you like to do with {item}?')
    print('1) Equip Item')
    print('2) Use Item')
    print('3) Discard Item')
    print('4) Return to Inventory')
    
    action = input('Choose an option (1-4): ').strip()
    while action not in ['1', '2', '3', '4']:
        action = input('Invalid choice').strip()
    
    if action == '1':  # Equip Item
        equipItem(item)
    elif action == '2':  # Use Item
        useItem(item)
    elif action == '3':  # Discard Item
        discardItem(item)
    elif action == '4':  # Return
        print('Returning to inventory...\n')
        
def equipItem(item):
    # Check if the item exists shop_item_descriptions
    if item not in shop_item_descriptions:
        print(f'{item} does not exist.')
        return
    if shop_item_descriptions[item][1] != 'Equipment': #verifies "Equipment" status
        print(f'{item} is not an equippable item.')
        return

    # Check for combat stats
    if item in item_combat_stats:
        attack, defense, health, slot = item_combat_stats[item]

        # Handle if the slot is already occupied
        if slot in player_stats['equipment']:
            unequipped_item = player_stats['equipment'][slot]
            print(f"You unequip {unequipped_item}.")
            unequipItem(unequipped_item)  # Reset stats when unequipping

        # Equip the new item
        player_stats['equipment'][slot] = item
        player_stats['attack'] += attack
        player_stats['defense'] += defense
        player_stats['health'] += health
        print(f"You have equipped {item}.")
    else:
        print(f"{item} cannot be equipped.\n")

def useItem(item): 
    if shop_item_descriptions[item][1] == 'Consumable':  # Ensure the item is usable
        if item in healing_amount:
            player_stats['health'] = min(startingHP, player_stats['health'] + healing_amount[item])  # Capping health at max
            print(f'You regained {healing_amount[item]} health!')
            player_stats['inventory'][item] -= quantity # Remove one instance of the item from inventory
    else:
        print(f"{item} cannot be used in this way.")
        
def discardItem(item):
    quantity = int(input(f"How many {item}(s) would you like to discard? "))
    removeFromInventory(item, quantity)

        
def checkInventory():
    print('\nYour Inventory:')
    if player_stats['inventory']:  # Check if inventory is not empty
        for item, quantity in player_stats['inventory'].items():
            print(f'{item}: {quantity}')
        selected_item = input("Select an item. Type 'exit' to quit.\n ").strip().title()

        if selected_item.lower() == 'exit':  # Option to exit the inventory check
            return
        if selected_item in player_stats['inventory']:
            #print(f'{shop_item_descriptions[item][]}')
            itemMenu(selected_item)  # Calls a function to handle item actions
        else:
            print("That item is not in your inventory.")
    else:
        print("There's nothing in there.\n")

def addToInventory(item, quantity=1):  # Add items to inventory
    if item in player_stats['inventory']:
        player_stats['inventory'][item] += quantity
    else:
        player_stats['inventory'][item] = quantity
    print(f"{quantity} {item}(s) added to your inventory.")
    
def removeFromInventory(item, quantity=1):  # Remove items from inventory
    if item in player_stats['inventory']:
        if player_stats['inventory'][item] >= quantity:
            player_stats['inventory'][item] -= quantity
            print(f"{quantity} {item}(s) removed from your inventory.")
            if player_stats['inventory'][item] == 0:  # Remove item if quantity reaches 0
                del player_stats['inventory'][item]
                print(f"{item} has been removed from your inventory.")
        else:
            print(f"You don't have enough {item}(s) to remove.")
    else:
        print(f"{item} is not in your inventory.")
