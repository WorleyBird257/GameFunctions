import random, gameUserInventory
from gameData import shop_item_descriptions, healing_amount, player_stats

shop_items = { #item name : (price, stock)
    'Apple': (10, 5),
    'Small Potion': (20, 3),
    'Longsword': (35, 1),
    'Rusty Shield': (35, 1),
    'Elixer': (50, 4),
    'Bomb': (100, 1)
    }

def purchase_shop_menu(items):
    '''
    Displays items in shop_items dictionary available for purchase in a stylized menu.
    Based on code in gameFunctions.

    Parameter: shop_item dictionary

    Returns: None
    '''
    print(' ' + '_' * 24 + ' ')
    print('|' + '*' + ' ' * 22 + '*' + '|')
    for item, (price, stock) in shop_items.items():
        if stock > 0:
            dollarPrice = f'${price:.2f}'
            print('|' + f'{item:<12} ({stock})' + f'{dollarPrice:>8}' + '|')
    print('|' + '_' * 24 + '|')

startingGold = player_stats['gold'] 
def gameShopLoop(startingGold):
    '''
    Shop loop. Allows for purchasing items and adds to inventory.
    Uses purchaseItem function to check quanitity and money available.
    Shop inventory changes after purchasing with loop breaking after user input or by emptying store's inventory.

    Parameter: player_stats['gold']

    Returns: None
    '''

def gameShopLoop(player_stats):
    '''
    Shop loop. Allows for purchasing items and adds to inventory.
    Uses purchaseItem function to check quantity and money available.
    Shop inventory changes after purchasing with loop breaking after user input or by emptying the store's inventory.

    Parameter: player_stats (dict)

    Returns: None
    '''
    while player_stats['gold'] > 0:  # Shop is open if the player has money
        if all(stock <= 0 for _, (_, stock) in shop_items.items()):  # Shop closes if everything is purchased
            print("The door is locked. A sign on the window says\nOut of inventory, come back later!\n")
            break

        # Normal shop loop
        print('\nWelcome to Griz Market!')
        print(f'You have {player_stats["gold"]}GP available')
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
        if player_stats['gold'] < total_cost:
            print('\nYou don\'t have enough gold to purchase that.')
            continue

        # Purchase items and update stats
        player_stats['gold'] -= total_cost  # Update gold directly in player_stats
        gameUserInventory.addToInventory(chosen_item, quantity_to_purchase)  # Update inventory
        shop_items[chosen_item] = (item_price, item_stock - quantity_to_purchase)  # Update shop inventory

        # Print purchase summary
        print(f'You bought {quantity_to_purchase} {chosen_item}(s). Remaining money: ${player_stats['gold']:.2f}')

        # Exit if no gold left
        if player_stats['gold'] <= 0:
            print('\nYou don\'t have enough gold to purchase anything.')
            print('The shopkeeper kicks you out!\n')
            break
    
if __name__ == '__main__':
    #startingGold = 100 #variable can be used outside of module
    gameShopLoop(startingGold)
