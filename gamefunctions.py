'''
Actionable functions for a game.

Four functions are present:
-purchase_item(itemPrice, startingMoney, quantityToPurchase)
-new_random_monster(monster_name)
-print_welcome(name)
-print_shop_menu(item1Name, item1Price, item2Name, item2Price)
'''

# Adventure Functions
# Reya Worley
# gamefunctions.py

#################################################################

import random # all variables are randomized for this function

itemPrice = float(random.randint(1, 100))
startingMoney = float(random.randint(1, 1000))
quantityToPurchase = int(random.randint(1, 100))

def purchase_item(itemPrice, startingMoney, quantityToPurchase):
    '''
    Purchases items without spending more money than available.

    Parameters:
        itemPrice (float)
        startingMoney (float)
        quanitityToPurchase (int)

    Returns:
        remaining_money, purchasedQuantity
    '''
    
    maxItems = startingMoney // itemPrice  # max allowed items to purchase 
    purchasedQuantity = min(quantityToPurchase, maxItems)  # limits items purchased (no negative integers)
    purchase_value = itemPrice * purchasedQuantity  # calculates the value based on purchasedQuantity
    remaining_money = startingMoney - purchase_value  # calculates the difference between starting money and what's left
    
    return purchasedQuantity, remaining_money

##################################################################

def new_random_monster(monster_name=None): 
    '''
    Creates a monster with randomized health, power, and money values associated to name and a brief description.

    Parameters:
        monster_name (str)

    Returns:
        monster_values (dict)

    Example:
        >>> new_random_monster('Goblin')
    '''
    
    monster_values_dict = { #first dictionary holds name and values for "stats"
        'Goblin': {'health': random.randint(140, 160), 'power': random.randint(15, 30), 'money': random.randint(1, 10)},
        'Draugr': {'health': random.randint(140, 175), 'power': random.randint(15, 25), 'money': random.randint(1, 15)},
        'Bat': {'health': random.randint(50, 80), 'power': random.randint(10, 25), 'money': random.randint(1, 7)},
        'Wolf': {'health': random.randint(150, 180), 'power': random.randint(15, 20), 'money': random.randint(5, 15)},
        'Skeleton': {'health': random.randint(160, 200), 'power': random.randint(20, 40), 'money': random.randint(10, 25)}
    }

    monster_description_dict = { #second dictionary holds monster name with description. Ties the two together
        'Goblin': 'Just a greedy little green guy!',
        'Draugr': 'A soulless corpse risen through necromancy',
        'Bat': 'Definitely not a vampire in disguise.',
        'Wolf': 'Lonely and hungry',
        'Skeleton': 'What is dead may never die.'
    }
    
    if monster_name is None: #allows for testing of a monster with different values with same name
        monster_name = random.choice(list(monster_values_dict.keys()))
        
    monster_values = monster_values_dict[monster_name]
        
    return { #outputs dictionary of monster name, description, and (randomized values). feels rough, would rather it output cleaner.
        'name': monster_name,
        'description': monster_description_dict[monster_name],
        'health': monster_values['health'],
        'power': monster_values['power'],
        'money': monster_values['money']
        }

#########################################################
 
def print_welcome(name='Reya'): 
    '''
    Prints a welcome banner where a given name is centered in a 20 character field.
    
    Parameters:
        name

    Returns:
        None
    '''
    nameLength = len(name)
    #fieldWidth = 20 - nameLength #keeps uniform width with various length name
    return f'{' Welcome, ' + name:^20}'

##########################################################

def print_shop_menu(item1Name='Potion', item1Price=50, item2Name='Elixir', item2Price=75): #my god, it's even got a border 
    '''
    Prints a sign from a list of two items with their corresponding prices.

    Item name field is 12 characters, item price field is 8 characters
    and prices have 2 decimal places with dollar sign ie) $12.34.
    
    Parameters:
        item1Name
        item1Price
        item2Name
        item2Price
    '''

    itemWidth = 12
    pricePrecision = 2
    priceWidth = 8
    
    item1PriceWidth = len(str(item1Price))
    priceWidth = abs(item1PriceWidth - pricePrecision)
    
    item2PriceWidth = len(str(item2Price))
    priceWidthBuffer = abs(5- item2PriceWidth)
    priceWidth = item2PriceWidth + (4 - priceWidthBuffer)

    print(' ' + '_' * 18 + ' ')
    print('|' + '*' + ' ' * 16 + '*' + '|')
    print('|' + f'{item1Name:<{itemWidth}}' + f'${item1Price:>{priceWidth}.{pricePrecision}f}' + '|')
    print('|' + f'{item2Name:<{itemWidth}}' + f'{'$':>}{item2Price:>{priceWidth}.{pricePrecision}f}' + '|')
    print('|' + ' ' * 18 + '|')
    print('|' + '_' * 18 + '|')
    
# Insane debugging. still doesn't work for price values of 5 index. 
    #print(len((' ' + '_' * 18 + ' ')))
    #print(len(('|' + '*' + ' ' * 16 + '*' + '|')))
    #print(len(('|' + f'{item1Name:<{itemWidth}}' + f'${item1Price:>{priceWidth}.{pricePrecision}f}' + '|')))
    #print(len(('|' + f'{item2Name:<{itemWidth}}' + f'{'$':>}{item2Price:>{priceWidth}.{pricePrecision}f}' + '|')))
    #print(len(('|' + ' ' * 18 + '|')))
    #print(len(('|' + '_' * 18 + '|')))

    #print(item1PriceWidth)
    #print(item2PriceWidth)
    #print(priceWidthBuffer)
          
item1Name = str()
item1Price = float()
item2Name = str()
item2Price = float()

#limitations of the formatting, changing the "size" of the price
# changes the width of the formatting.
# can't figure out how to have '$' stay consistent

##################################################################

#Test Code #
if __name__ in '__main__': #purchase_item
    def test_functions():
        print(purchase_item(1.58, 100, 3))
        print(purchase_item(itemPrice, startingMoney, quantityToPurchase))
        print(purchase_item(itemPrice, startingMoney, quantityToPurchase=1)) #default quantity

        print(new_random_monster()) #new_random_monster
        monster_name = 'Goblin' # same monster name but with different properties
        monster1 = new_random_monster(monster_name)
        monster2 = new_random_monster(monster_name)
        print(monster1)
        print(monster2)

        print(print_welcome()) #4 #welcome, with different names
        print(print_welcome(name='Gerald')) #6
        print(print_welcome('Guinnivere')) #10

        print_shop_menu()
        print_shop_menu(item1Name, item1Price, item2Name, item2Price)
        print_shop_menu('Apple', 31.5, 'Orange', 3.2)

    print(test_functions())
