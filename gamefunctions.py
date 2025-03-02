# Adventure Functions
# 2/15/25, 3/1/25
# Reya Worley
# gamefunctions.py

import random

# all variables are randomized

#################################################################
#      purchase Item function

itemPrice = float(random.randint(1, 100))
startingMoney = float(random.randint(1, 1000))
quantityToPurchase = int(random.randint(1, 100))

def purchase_item(itemPrice, startingMoney, quantityToPurchase):
    ''' function purchases items without spending more money than available
    Three parameters: itemPrice, startingMoney, quanitityToPurchase
    -limits quantity to available purchasing power
    -default value = 1
    -shows correct change after purchase'''
    maxItems = int(startingMoney // itemPrice)  # max allowed items to purchase 
    purchasedQuantity = min(quantityToPurchase, maxItems)  # limits items purchased (no negative integers)
    purchase_value = itemPrice * purchasedQuantity  # calculates the value based on purchasedQuantity
    remaining_money = startingMoney - purchase_value  # calculates the difference between starting money and what's left
    
    return f'Items purchased: {purchasedQuantity}\nRemaining money: {remaining_money}\n'

#Test Code
if __name__ in '__main__':
    print(purchase_item(1.58, 100, 3))
    print(purchase_item(itemPrice, startingMoney, quantityToPurchase))
    print(purchase_item(itemPrice, startingMoney, quantityToPurchase=1)) #default quantity

##################################################################

# Create a random Monster:
#output is the profile of a monster based on 5 options with random integers for health, power, and money. 

def new_random_monster(monster_name=None): #first dictionary holds name and values for "stats"
    ''' Creates monster with random values.
    Monster has 'health, power, and money' associated to name.
    Monstere includes a brief description. '''
    monster_values_dict = {
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

# Example usage:
print(new_random_monster())

# example to show the same monster name but with different properties
monster_name = 'Goblin'
monster1 = new_random_monster(monster_name)
monster2 = new_random_monster(monster_name)

print(monster1)
print(monster2)

########################################################################
########################################################################
#Assignment 6


#   Welcome!
def print_welcome(name='Reya'): 
    '''prints welcome with 'name' parameter
    output is centered in 20 character field'''
    return f'{'Welcome, ' + name:^20}'

if __name__ in '__main__':
    print(print_welcome()) #4
    print(print_welcome(name='Gerald')) #6
    print(print_welcome('Guinnivere')) #10

##########################################################
#   Formatted shop sign, 
def print_shop_menu(item1Name='Potion', item1Price=50, item2Name='Elixir', item2Price=75): #my god, it's even got a border 
    '''prints sign with list of two items and corresponding prices
    item name field is 12 characters, item price field is 8 characters
    prices have 2 decimal places with dollar sign ie) $12.34
    parameters: item1Name, item1Price, item2Name, item2Price
    '''

    itemWidth = 12

    item1PriceWidth = len(str(item1Price))
    priceWidth = abs(5-item1PriceWidth)
    

    item2PriceWidth = len(str(item2Price))
    priceWidthBuffer = abs(5- item2PriceWidth)
    priceWidth = item2PriceWidth + (4 - priceWidthBuffer)
    
    pricePrecision = 2


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
if __name__ in '__main__':
    print_shop_menu()
    print_shop_menu(item1Name, item1Price, item2Name, item2Price)
    print_shop_menu('Apple', 31.5, 'Orange', 3.2)


#limitations of the formatting, changing the "size" of the price
# changes the width of the formatting.
# can't figure out how to have '$' stay consistent



