import random, gameUserInventory
from gameData import shop_item_descriptions, Player

def purchase_shop_menu(items):
    '''
    Displays items in a stylized menu.

    Parameters:
            items (dict): dictionaries of items to be displayed 

    Returns: None
    '''
    print(' ' + '_' * 25 + ' ')
    print('|' + '*' + ' ' * 23 + '*' + '|')
    for item, (price, stock) in items.items():
        if stock > 0:
            dollarPrice = f'${price:.2f}'
            print('|' + f'{item:<13} ({stock})' + f'{dollarPrice:>8}' + '|')
    print('|' + '_' * 25 + '|')

def run_shop_loop(player_instance, shop_items, shop_name):
    '''
    Shop loop. Allows for purchasing items and adds to inventory.
    Uses purchaseItem function to check quantity and money available.
    Shop inventory changes after purchasing with loop breaking after user input or by emptying the store's inventory.

    Parameter: player_instance_stats (Player): current instance of player
               shop_items (dict): dictionary with price, stock tuple
               shop_name (str): Name of the shop

    Returns: None
    '''
    while player_instance.gold > 0:  # Shop is open if the Player has money

        if all(stock <= 0 for _, (_, stock) in shop_items.items()):  # Shop closes if everything is purchased
            print(f"{shop_name}\'s door is locked. A sign on the window says\nOut of inventory, come back later!\n")
            break

        # Normal shop loop
        print('\nWelcome to {shop_name}!')
        print(f'You have {player_instance.gold}GP available')
        purchase_shop_menu(shop_items)
        
        # User chooses an item to purchase
        chosen_item = input('\nEnter the name of the item you\'d like to purchase.\nOr type "exit" to leave: ').strip().title()
        if chosen_item.lower() == 'exit':  # Exit shop
            print('You exit the shop.\n')
            break

        # Verifies purchase (item name)
        if chosen_item not in shop_items:
            print('Sorry, I don\'t have any of that item.')
            continue

        # Verifies item stock
        item_price, item_stock = shop_items[chosen_item]
        if item_stock <= 0:
            print(f'Sorry, {chosen_item} is out of stock!')
            continue
        
        # Quantity to purchase
        quantity_to_purchase = int(input('How many? '))
        if quantity_to_purchase > item_stock:
            print(f'There are only {item_stock} {chosen_item}(s) left. You bought the remaining {item_stock}.')
            quantity_to_purchase = item_stock

        total_cost = item_price * quantity_to_purchase

        # If there's not enough money to purchase
        if player_instance.gold < total_cost:
            print('\nYou don\'t have enough gold to purchase that.')
            continue

        # Purchase items and update inventory
        player_instance.gold -= total_cost  # Update gold directly in Player_stats
        player_instance.add_to_inventory(chosen_item, quantity_to_purchase)  # Update inventory
        shop_items[chosen_item] = (item_price, item_stock - quantity_to_purchase)  # Update shop inventory

        # Print purchase summary
        print(f'You bought {quantity_to_purchase} {chosen_item}(s). Remaining money: ${player_instance.gold:.2f}')

        # Exit if no gold left
        if player_instance.gold <= 0:
            print('\nYou don\'t have enough gold to purchase anything.')
            print('The shopkeeper kicks you out!\n')
            break
        
def game_shop_loop(player_instance):
    ''' plugs into run_shop_loop to access general shop'''
    
    shop_items = {
        'Apple': (10, 5),
        'Small Potion': (20, 3),
        'Longsword': (35, 1),
        'Rusty Shield': (35, 1),
        'Elixir': (50, 4),
        'Bomb': (100, 1)
    }
    run_shop_loop(player_instance, shop_items, "Griz Market")

def game_blacksmith_loop(player_instance):
    '''
    Blacksmith allows for repairing damaged items.
    Allows for upgrading items with crafting materials. #FIXME

    Returns: None
    '''
    print("\nMonte\'s Forge")

    while True:  # Keeps the loop running until the player exits
        print('What can we help with today?')
        print('1) Repair equipment')
        print('2) Browse blacksmith\'s shop')
        print('3) Forge a new weapon')
        print('4) Exit')

        choice = input('Select an option: ').strip()
        
        if choice == '1': #Repair Equipment
            repairable_items = {}
        
            # Gather items that need repair
            for item, quantity in player_instance.inventory.items():
                item_data = shop_item_descriptions.get(item, {})
                current_durability = item_data.get("Durability", -1)  # Default to -1 for debugging
                max_durability = item_data.get("Max Durability", current_durability)
                
                #print(f"Checking {item}: Durability {current_durability}/{max_durability}")  # Debug check
                if current_durability < max_durability:
                    repairable_items[item] = (max_durability - current_durability) * 2
            
            if repairable_items: # Check to see if any repairable items were found in the dictionary
                print("Repairable Items:")
                for item, cost in repairable_items.items():
                    durability = shop_item_descriptions[item].get("Durability", 0)
                    max_durability = shop_item_descriptions[item].get("Max Durability", durability)
                    print(f"{item}: {durability}/{max_durability} - Repair Cost: {cost}GP\n")

                selected_item = input("Select an item to repair or type 'exit': ").strip().title()

                if selected_item.lower() == "exit":
                    print("You leave the forge.\n")
                    break  # Exit the loop properly

                if selected_item in repairable_items and player_instance.gold >= repairable_items[selected_item]: #checks money available o repair versus repair
                    item_data = shop_item_descriptions[selected_item]
                    item_data["Durability"] = item_data.get("Max Durability", item_data["Durability"])  # Fully restore durability
                    
                    player_instance.gold -= repairable_items[selected_item]
                    print(f"{selected_item} has been fully repaired!")
                else: 
                    print("Not enough gold or invalid item selection.")

            else:
                print("No items need repair.")
                break  # If nothing needs repair, exit the blacksmith loop
            
        elif choice == '2': #Blacksmith Shop
            blacksmith_items = {
                "Steel Sword": (75, 1),
                "Iron Shield": (80, 1),
                "Leather Armor": (120, 1),
                }
            run_shop_loop(player_instance, blacksmith_items, "Monte's Blacksmith Shop")
                     
        elif choice == '3': # Forge Weapons
            pass #FIXME
        
        elif choice == '4': #Exit
            print('You leave the forge.')
            break
        else:
            print('Invalid choice. Try again,') 
            
            
    
#if __name__ == '__main__':
    
    #game_shop_loop(player_instance)
