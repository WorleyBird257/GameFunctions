import pygame
import gameCombatLoop
from wanderingMonster import WanderingMonster
from gameData import game_map                   #<<<< I know this is a lot, but it's better then 
from gameData import player_stats           #<<<< module dependencies and allows each module to call upon a set of data. 
from gameData import tileSize, MapHeight, MapWidth, SCREEN_WIDTH, SCREEN_HEIGHT, colors, town_x, town_y

monsters = WanderingMonster.generate_initial_monsters() #******

#player initialization:
player_move_counter = 0 #initialize steps
player_x, player_y = player_stats.get('position', (4,5))
player_rect = pygame.Rect(player_x * tileSize, player_y * tileSize, tileSize, tileSize)

def draw_map(screen, game_map):
    for row in range(MapHeight):
        for col in range(MapWidth):
            tile = game_map[row][col]
            pygame.draw.rect(screen, colors[tile], pygame.Rect(col * tileSize, row * tileSize, tileSize, tileSize))

def explore_map(player_x, player_y, player_stats, monsters, player_move_counter):
    pygame.init() #initialize game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #screen size
    clock = pygame.time.Clock() 
    player_stats['position'] = (player_x, player_y)
    left_town = False #doesnt immediately break loop if player starts on town square
    movement_cooldown = 1.5
    move_timer = movement_cooldown 
    
    running = True
    while running:
        screen.fill((0,0,0)) # colors frame black, "erasing" blur
        draw_map(screen, game_map)  # render map
    
        #draw objects
        pygame.draw.circle(screen, (0, 200, 0), (town_x * tileSize + 16, town_y * tileSize + 16), 16) #draws town "green"
        pygame.draw.rect(screen, (209, 237, 242), player_rect) # draws player "pale blue"
        for monster in monsters: #draws monsters based on RGB values
            pygame.draw.circle(screen, monster.color, (monster.x * tileSize + 16, monster.y * tileSize + 16), 16)
        
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allows exiting with ESC
                    running = False

        key = pygame.key.get_pressed()
        prev_x, prev_y = player_x, player_y  

        #arrow directions and handling
        if move_timer <= 0:
            moved = False # unlike with static monster iteration, the loop was continous
                            #flag manages to track player movement
            if key[pygame.K_UP] and player_y > 0:
                player_y -= 1
                moved = True
            if key[pygame.K_DOWN] and player_y < MapHeight - 1:
                player_y += 1
                moved = True
            elif key[pygame.K_LEFT] and player_x > 0:
                player_x -= 1
                moved = True
            elif key[pygame.K_RIGHT] and player_x < MapWidth - 1:
                player_x += 1
                moved = True
            if moved:
                move_timer = movement_cooldown
                player_move_counter += 1

                if player_move_counter % 2 == 0: #monster moves every two player moves
                    for monster in monsters:
                        monster.move()
                if player_move_counter % 5 == 0 and len(monsters) <= 1:  #every 5 moves if there's less than one monster, a monster respawns on map
                    monsters.extend(WanderingMonster.generate_initial_monsters())
        else:
            move_timer -= 1
            
        #updates player position
        player_rect.topleft = (player_x * tileSize, player_y * tileSize)
        player_stats['position'] = (player_x, player_y)  

        if (player_x, player_y) != (town_x, town_y):
            left_town = True

        # Town return logic
        if player_x == town_x and player_y == town_y:
            if left_town:  # Only exit if player has left town at least once
                print("Returning to town menu...")
                running = False

        #monster encounter
        for monster in monsters[:]:
            if (player_x, player_y) == (monster.x, monster.y):
                print('A branch snaps nearby!')
                player_stats = gameCombatLoop.fightMonster(player_stats, monster)
                monsters.remove(monster)  

        pygame.display.update()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':

    explore_map(player_x, player_y, player_stats, monsters, player_move_counter)
   
