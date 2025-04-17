shop_item_descriptions = {  # binds shop_item elements with durability, item type, description, effect
    'Apple': (1, 'Consumable', 'A shiny red apple.', 'Heals 10 health while in combat.'),
    'Small Potion': (1, 'Consumable', 'A milky liquid swirls in a flask.', 'Heals 25 health in combat.'),
    'Longsword': (100, 'Equipment', 'A weathered but trusty weapon.', 'Raises attack power by 15'),
    'Rusty Shield': (100, 'Equipment', 'Scratches and dents mar the surface.', 'Raises defense by 5'),
    'Elixer': (1, 'Consumable', 'Silver liquid swirls in a round bottle.', 'Used in battle, the user will regain 50 health.'),
    'Bomb': (1, 'Consumable', 'A round, black item with a wick on one end.', 'Instantly kills one enemy. Single Use.')
}

item_combat_stats = { #name (attack, defense, health, equipment slot)
    'Longsword': (15, 0, 0, 'hand'),
    'Rusty Shield': (0, 15, 0, 'off hand')
    }

healing_amount = {
    "Apple": 10,
    "Small Potion": 25,
    "Elixer": 50
}

player_stats = {
    "name": "Adventurer",
    "attack": 10,
    "defense": 10,
    "health": 50,
    "gold": 100,
    "experience": 0,
    "inventory": {},
    "equipment": {},
    "position": (4, 5),  # Default spawn at town
}
inventory = player_stats['inventory']


#initialize map variables
tileSize = 32
MapWidth = 10
MapHeight = 10 
SCREEN_WIDTH = tileSize * MapWidth
SCREEN_HEIGHT = tileSize * MapHeight

colors = {
    0: (0, 0, 0),  # Empty
    1: (0, 200, 0),  # Town
    2: (34, 139, 34),  # Forest
    3: (139, 69, 19),  # Road
    4: (0, 0, 255),  # Water 
    5: (194, 178, 128),  # Sand
    6: (255, 0, 0) #monster 
}

#map and town positions:
town_x, town_y = 4, 5

# 0 = Empty, 1 = Town, 2 = Forest, 3 = Road, 4 = water, 5 = sand 6 = enemy
game_map = [
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 2],
    [0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 5, 5],
    [2, 2, 2, 0, 0, 0, 0, 4, 4, 4],
    [2, 2, 2, 0, 0, 5, 4, 5, 0, 0]
]
