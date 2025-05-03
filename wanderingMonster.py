import random
import pygame
from gameData import tileSize, MapHeight, MapWidth, SCREEN_WIDTH, SCREEN_HEIGHT, colors, town_x, town_y

class WanderingMonster:
    """Represents a roaming monster in the game world."""

    monster_values_dict = {
        'Goblin': {'color': (224, 163, 46), 'health': (120, 135), 'power': (15, 30), 'gold': (10, 25), 'experience': (15, 30)},
        'Draugr': {'color': (157, 188, 64), 'health': (130, 150), 'power': (15, 25), 'gold': (10, 19), 'experience': (15, 30)},
        'Bat': {'color': (80, 80, 80), 'health': (50, 80), 'power': (10, 25), 'gold': (7, 17), 'experience': (15, 30)},
        'Wolf': {'color': (51, 102, 102), 'health': (150, 160), 'power': (15, 20), 'gold': (10, 15), 'experience': (15, 30)},
        'Skeleton': {'color': (160, 160, 160), 'health': (160, 175), 'power': (20, 30), 'gold': (18, 25), 'experience': (15, 30)}
    }

    monster_description_dict = {
        'Goblin': 'Just a greedy little green guy!',
        'Draugr': 'A soulless corpse risen through necromancy',
        'Bat': 'Definitely not a vampire in disguise.',
        'Wolf': 'Lonely and hungry',
        'Skeleton': 'What is dead may never die.'
    }

    @staticmethod #allows for the random integer function to work within the class 
    def random_stat(min_val, max_val):
        """Produces a random integer based on a range between two values."""
        return random.randint(min_val, max_val)

    def __init__(self, name=None, x=None, y=None, monster_type=''):  
        """Initializes a new random wandering monster."""
        if name is None: #spin the wheel!
            name = random.choice(list(self.monster_values_dict.keys()))

        self.name = name
        self.description = self.monster_description_dict[name]
        self.color = self.monster_values_dict[name]['color']
        self.health = self.random_stat(*self.monster_values_dict[name]['health'])
        self.gold = self.random_stat(*self.monster_values_dict[name]['gold'])
        self.power = self.random_stat(*self.monster_values_dict[name]['power'])
        self.experience = self.random_stat(*self.monster_values_dict[name]['experience'])

        self.monster_type = monster_type #added so I can have pictures

        self.image = self.get_monster_image()  # Load image once and store it ******
        # Assign a random starting position (not in town)
        self.x = x if x is not None else random.randint(0, MapWidth - 1)
        self.y = y if y is not None else random.randint(0, MapHeight - 1)

        # Ensure monster does not spawn in town
        while (self.x, self.y) == (town_x, town_y):
            self.x = random.randint(0, MapWidth - 1)
            self.y = random.randint(0, MapHeight - 1)
            
    def get_monster_image(self):
        try:
            #print(f"Loading image for {self.name}")  # Debugging line to check load frequency

            if self.monster_type == 'Bat':
                return pygame.image.load("assets/sprite_bat.png")
            elif self.monster_type == 'Goblin':
                return pygame.image.load("assets/sprite_goblin.png")
            elif self.monster_type == 'Skeleton':
                return pygame.image.load("assets/sprite_skele.png")
            elif self.monster_type == 'Wolf':
                return pygame.image.load("assets/sprite_wolf.png")
            elif self.monster_type == "Draugr":
                return pygame.image.load("assets/sprite_zombie.png")
            else:
                return None
        except pygame.error:
            print(f"Image for {self.monster_type} not found. Using fallback.")
            placeholder = pygame.Surface((tileSize, tileSize))
            placeholder.fill(self.color)  # Uses monster's assigned color
            return placeholder  # Ensures every monster has an image
        
    def draw(self, screen):
        """Handles rendering the monster."""
        try:
            if self.image:
                screen.blit(self.image, (self.x * tileSize, self.y * tileSize))
            else:
                pygame.draw.circle(screen, self.color, (self.x * tileSize + 16, self.y * tileSize + 16), 16)  # Placeholder
        except pygame.error:
            print(f"Image file not found for {self.name}. Defaulting to shapes.")
            
    def move(self):
        """Moves the monster in a random direction, ensuring it stays within grid bounds."""
        while True:  # Loop until a valid move is found
            direction = random.choice(["up", "down", "left", "right"])

            new_x, new_y = self.x, self.y
            if direction == "up" and self.y > 0:
                new_y -= 1
            elif direction == "down" and self.y < MapHeight - 1:
                new_y += 1
            elif direction == "left" and self.x > 0:
                new_x -= 1
            elif direction == "right" and self.x < MapWidth - 1:
                new_x += 1

            # Ensure monster does not move into the town square
            if (new_x, new_y) != (town_x, town_y):
                self.x, self.y = new_x, new_y
                break  # Valid move found, exit loop
            
    def __repr__(self): #for debugging, shows monster and position in string format
        """Returns a detailed string representation of the monster."""
        return f"{self.name} ({self.description}) at ({self.x}, {self.y}) with {self.health} HP, {self.gold} gold"

    @classmethod #allows scalability with creating monsters instead of creating instances repeatedly
    def generate_initial_monsters(cls, count=2):
        """Creates the initial set of monsters at game start."""
        monster_types = ['Bat', 'Goblin', 'Skeleton', 'Wolf', 'Draugr']  # Define types
        monsters = []

        for _ in range(count):  # Generate 5 monsters
            name = random.choice(monster_types)
            x = random.randint(0, MapWidth - 1)
            y = random.randint(0, MapHeight - 1)
            #monster_type = random.choice(monster_types)
            monsters.append(cls(name=name, x=x, y=y, monster_type=name))

        return monsters
        #return [cls() for _ in range(count)]
