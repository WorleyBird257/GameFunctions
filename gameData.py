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
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 2, 2],
    [2, 2, 2, 0, 0, 0, 0, 2, 2, 2],
    [2, 2, 2, 0, 0, 2, 2, 2, 0, 0]
]

class Player:
        # Initialize player stats
    def __init__(self, name="Adventurer", health=50, gold=100, position=(4, 5)):
        self.name = name
        self.health = health
        self.max_health = health
        self.gold = gold
        self.experience = 0
        self.inventory = {} #contains all items held/ bought
        self.equipment = {} #contains stat enhancing items (applys to combat)
        self.attack = 10
        self.defense = 5
        self.position = position #stored as tuple
        self.map_height = MapHeight
        self.map_width = MapWidth

    def to_dict(self): #serialize to dictionary
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "gold": self.gold,
            "experience": self.experience,
            "inventory": self.inventory,
            "equipment": self.equipment,
            "attack": self.attack,
            "defense": self.defense,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(
            name=data["name"],
            health=data["health"],
            gold=data["gold"],
            position=tuple(data["position"])
        )
        player.max_health = data["max_health"]
        player.experience = data["experience"]
        player.inventory = data["inventory"]
        player.equipment = data["equipment"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        return player

    @property #allows for x coordinate to be checked 
    def player_x(self):
        return self.position[0]
    @player_x.setter
    def player_x(self, value):
        self.position = (value, self.position[1])
    @property
    def player_y(self): #allows for y coordinate to be checked
        return self.position[1]
    @player_y.setter
    def player_y(self, value):
        self.position = (self.position[0], value)

    def move(self, direction):
        if direction == "up" and self.player_y > 0:
            self.player_y -= 1
        elif direction == "down" and self.player_y < MapHeight - 1:
            self.player_y += 1
        elif direction == "left" and self.player_x > 0:
            self.player_x -= 1
        elif direction == "right" and self.player_x < MapWidth - 1:
            self.player_x += 1


        # Inventory management
    def add_to_inventory(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        print(f"{quantity} {item}(s) added to your inventory.")

    def remove_from_inventory(self, item, quantity=1):
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            #print(f"{quantity} {item}(s) removed from your inventory.")
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            print(f"You don't have enough {item}(s) to remove.")

        # Equipment management
    def equip_item(self, item):
        # Check if the item exists and is equippable
        if item not in shop_item_descriptions or shop_item_descriptions[item][1] != "Equipment":
            print(f"{item} is not an equippable item.")
            return

        if item in item_combat_stats:
            attack, defense, health, slot = item_combat_stats[item]

            # Unequip existing item in the same slot
            if slot in self.equipment:
                unequipped_item = self.equipment[slot]
                print(f"You unequip {unequipped_item}.")
                old_attack, old_defense, old_health, _ = item_combat_stats[unequipped_item]
                self.attack -= old_attack
                self.defense -= old_defense
                self.health -= old_health

            # Equip new item
            self.equipment[slot] = item
            self.attack += attack
            self.defense += defense
            self.health = min(self.health + health, self.max_health)  # Cap health
            print(f"You have equipped {item}.")
            #print(f"Current stats: Attack={self.attack}, Defense={self.defense}, HP={self.health}.")
        else:
            print(f"{item} cannot be equipped.")

        # Combat health management
    def heal(self, item):
        if item in healing_amount:
            self.health = min(self.max_health, self.health + healing_amount[item])
            print(f"Healed by {healing_amount[item]}!")
            #print(f"Current HP: {self.health}")
            self.remove_from_inventory(item)
        else:
            print(f"{item} cannot be used for healing.")
