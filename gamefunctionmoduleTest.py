import gameFunctions, random

def choose_function(): #presents options for user inputs to call specifc fxn
    print('Select a function from list:')
    print('1. Purchase Item')
    print('2. Random Monster')
    print('3. Welcome')
    print('4. Shop Menu')

    option = input('Enter 1 - 4\n')

    if option == '1':
        print('Purchase Item')
        price = float(input('Item Price:\n'))
        money = float(input('Starting Money:\n'))
        quantity = int(input('Number to Purchase:\n'))
        
        result = gameFunctions.purchase_item(price, money, quantity)
        print(result)
    
    elif option == '2':
        print('Random Monster')
        print('Choose a Monster: Goblin, Draugr, Bat, Wolf, Skeleton')
        monster = input()
        
        result = gameFunctions.new_random_monster(monster)
        print(result) #clean up output and dictionaries
    
    elif option == '3':
        print('Welcome')
        name = input('Please type your name:\n')
        
        result = gameFunctions.print_welcome(name)
        print(result)
    
    elif option == '4':
        print('Shop Menu')
        name1 = input('Input 1st item in shop:\n')
        price1 = float(input('Input price of 1st item:\n'))
        name2 = input('Input 2nd item in shop:\n')
        price2 = float(input('Input price of 2nd item:\n'))

        result = gameFunctions.print_shop_menu(name1, price1, name2, price2)
        print(result) #ehhhhh
    else:
        print('Choose a number between 1 and 4')

        
if __name__ == '__main__':
    choose_function()
    

