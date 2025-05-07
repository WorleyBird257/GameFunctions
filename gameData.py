import pygame

shop_item_descriptions = { # binds shop_item elements with durability, item type, description, Effect/Combat Stats
    'Apple': {
        'Durability': 1,
        'Max Durability': 1,
        'Item Type': 'Consumable',
        'Description': 'A shiny red apple. Heals 10 health while in combat.',
        'Effect': 10,
    },
    'Small Potion': {
        'Durability': 1,  
        'Max Durability': 1,
        'Item Type': 'Consumable',
        'Description': 'A milky liquid swirls in a flask. Heals 25 health in combat.',
        'Effect': 25,
    },
    'Longsword': {
        'Durability': 100,
        'Max Durability': 100,
        'Item Type': 'Equipment',
        'Description': 'A weathered but trusty weapon. When equipped, raises attack power by 15.',
        'Combat stats': {
            'Attack': 15,
            'Defense': 0,
            'Stamina': 0,
            'Equipment Type': 'hand'
        },
    },
    'Rusty Shield': {
        'Durability': 100,
        'Max Durability': 100,
        'Item Type': 'Equipment',
        'Description': 'Scratches and dents mar the surface. When equipped, raises defense by 10.',
        'Combat stats': {
            'Attack': 0,
            'Defense': 10,
            'Stamina': 0,
            'Equipment Type': 'off hand'
        },
    },
    'Elixir': {  
        'Durability': 1,
        'Max Durability': 1,
        'Item Type': 'Consumable',
        'Description': 'Silver liquid swirls in a round bottle. Used in battle, the user will regain 50 health.',
        'Effect': 50,
    },
    'Bomb': {
        'Durability': 1,
        'Max Durability': 1,
        'Item Type': 'Consumable',
        'Description': 'A round, black item with a wick on one end. Instantly kills one enemy.',
    },
    'Steel Sword': {
        'Durability': 150,
        'Max Durability': 150,
        'Item Type': 'Equipment',
        'Description': 'A sturdy blade. A cold gleam reflects off the sharp edge. +23 Attack.',
        'Combat stats': {
            'Attack': 23,
            'Defense': 0,
            'Stamina': 0,
            'Equipment Type': 'hand',
        },
    },
    'Iron Shield': {
        'Durability': 150,
        'Max Durability': 150,
        'Item Type': 'Equipment',
        'Description': 'Reliable in the face of the enemy. +20 Defense.',
        'Combat stats': {
            'Attack': 0,
            'Defense': 20,
            'Stamina': 0,
            'Equipment Type': 'off hand',
        },
    },
    'Leather Armor': {
        'Durability': 120,
        'Max Durability': 120,
        'Item Type': 'Equipment',
        'Description': 'Studded leather armor, you feel stronger while wearing it. Slightly increases your Stamina and Defense.',  # Added missing comma
        'Combat stats': {
            'Attack': 0,
            'Defense': 15,
            'Stamina': 5,
            'Equipment Type': 'chest',
        },
    }
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
        self.image = self.load_player_image()  # Store image in Player instance

        
    def to_dict(self): #serializes data for saving to json
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "gold": self.gold,
            "experience": self.experience,
            "inventory": {
                item: {
                    "quantity": quantity,
                    "durability": shop_item_descriptions[item].get("Durability", 1)  # Ensure durability is saved
                }
                for item, quantity in self.inventory.items()
            },
            "equipment": self.equipment,
            "attack": self.attack,
            "defense": self.defense,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data): #extracts data from json back to class
        player = cls(
            name=data["name"],
            health=data["health"],
            gold=data["gold"],
            position=tuple(data["position"])
        )
        
        player.max_health = data["max_health"]
        player.experience = data["experience"]
        player.equipment = data["equipment"]
        player.attack = data["attack"]
        player.defense = data["defense"]

        # Restore inventory with durability
        player.inventory = {item: item_data["quantity"] for item, item_data in data["inventory"].items()}
        
        for item, item_data in data["inventory"].items():
            if item in shop_item_descriptions:
                shop_item_descriptions[item]["Durability"] = item_data.get("durability", shop_item_descriptions[item].get("Durability", 1))
        
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

    #initialize drawing player
    def load_player_image(self):
        try:
            return pygame.image.load("assets/sprite_character.png")
        except FileNotFoundError:
            print("FileNotFoundError: Player sprite not found. Using placeholder.")
            player_image = pygame.Surface((tileSize, tileSize))
            player_image.fill((209, 237, 242))
        except pygame.error:
            print("Player sprite not found, using placeholder.")
            placeholder = pygame.Surface((tileSize, tileSize))
            placeholder.fill((209, 237, 242))
            return placeholder
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
            #print(f"{quantity} {item}(s) removed from your inventory.") debugg line
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            print(f"You don't have enough {item}(s) to remove.")

    # Equipment management
    def equip_item(self, item):
        if item not in shop_item_descriptions or shop_item_descriptions[item].get("Item Type") != "Equipment":
            print(f'{item} is not an equippable item.')
            return

        item_data = shop_item_descriptions[item]
        combat_stats = item_data.get('Combat stats', {})

        attack = combat_stats.get('attack"', 0)
        defense = combat_stats.get('defense', 0)
        health = combat_stats.get("health", 0)
        slot = combat_stats.get('Equipment Type', None)

        if slot:
            # Unequip existing item in the same slot
            if slot in self.equipment:
                unequipped_item = self.equipment[slot]
                unequipped_stats = shop_item_descriptions[unequipped_item].get("Combat stats", {})
                old_attack = unequipped_stats.get('attack', 0)
                old_defense = unequipped_stats.get('defense', 0)
                old_health = unequipped_stats.get('stamina', 0)

                print(f'You unequip {unequipped_item}.')
                self.attack -= old_attack
                self.defense -= old_defense
                self.health -= old_health

            # Equip new item
            self.equipment[slot] = item
            self.attack += attack
            self.defense += defense
            self.health = min(self.health + health, self.max_health)  # Cap health
            print(f'You have equipped {item}.')
        else:
            print(f'{item} cannot be equipped.')

    # Combat equipment management
    def reduce_durability(self, item): 
        item_data = shop_item_descriptions.get(item, {})
        if not item_data: #checks if item is in the dictionary
            print(f"{item} does not have durability settings.") #debugg line
            return

        item_type = item_data.get("Item Type", "")
        durability = item_data.get("Durability", 0)

        if item_type == "Consumable": 
            print(f"You used {item}.")
            self.remove_from_inventory(item, 1)  # Fully removes the item
            return

        elif item_type == "Equipment": #weapons and armor will function differently
            item_data["Durability"] -= 2  # Reduce durability by 2 per use
            #print(f"{item} durability reduced to {item_data['Durability']}.") #debugg line

            if item_data["Durability"] <= 0:
                print(f"{item} has broken!/n {item} has been unequipped!")
                self.equipment = {slot: equipped for slot, equipped in self.equipment.items() if equipped != item}

    # Combat health management
    def heal(self, item):
        if item in shop_item_descriptions:
            heal_amount = shop_item_descriptions[item].get("Effect", 0)
            if heal_amount > 0:
                self.health = min(self.max_health, self.health + heal_amount)
                print(f'Healed by {heal_amount} HP!')
                self.remove_from_inventory(item)
            else:
                print(f'{item} cannot be used for healing.')
        else:
            print(f'{item} cannot be used that way.')
