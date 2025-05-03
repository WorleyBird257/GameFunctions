import pygame
import gameCombatLoop
from wanderingMonster import WanderingMonster
from gameData import game_map, tileSize, MapHeight, MapWidth, SCREEN_WIDTH, SCREEN_HEIGHT, colors, town_x, town_y, Player

monsters = WanderingMonster.generate_initial_monsters()
player_move_counter = 0  # Initialize steps

def draw_map(screen, game_map, player_instance, monsters):
    # Draw the map
    for row in range(MapHeight):
        for col in range(MapWidth):
            tile = game_map[row][col]
            pygame.draw.rect(screen, colors[tile], pygame.Rect(col * tileSize, row * tileSize, tileSize, tileSize))

    screen.blit(player_instance.image, (player_instance.position[0] * tileSize, player_instance.position[1] * tileSize))    # Draw monsters

    for monster in monsters:
        monster.draw(screen)  # Each monster now handles its own rendering
    
def explore_map(player_instance, monsters, player_move_counter):
    pygame.init()  # Initialize game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Screen size
    clock = pygame.time.Clock()

    left_town = False  # Player needs to leave town once to trigger return logic
    movement_cooldown = 1.5
    move_timer = movement_cooldown

    running = True
    while running:
        screen.fill((0, 0, 0))  # Colors frame black, "erasing" blur
        draw_map(screen, game_map, player_instance, monsters)  # Render map

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allows exiting with ESC
                    running = False

        key = pygame.key.get_pressed()

        # Handle movement with cooldown
        if move_timer <= 0:
            moved = False  # Track Player movement 
            if key[pygame.K_UP]:
                player_instance.move('up')
                moved = True
            elif key[pygame.K_DOWN]:
                player_instance.move('down')
                moved = True
            elif key[pygame.K_LEFT]:
                player_instance.move('left')
                moved = True
            elif key[pygame.K_RIGHT]:
                player_instance.move('right')
                moved = True

            if moved:
                move_timer = movement_cooldown
                player_move_counter += 1

                # Monster movement every two Player moves
                if player_move_counter % 2 == 0:
                    for monster in monsters:
                        monster.move()

                # Respawn monsters when none are left
                if len(monsters) == 0:
                    monsters.extend(WanderingMonster.generate_initial_monsters())
        else:
            move_timer -= 1

        # Town logic
        if player_instance.position != (town_x, town_y):
            left_town = True

        if player_instance.position == (town_x, town_y) and left_town:
            print("Returning to town menu...")
            running = False

        # Monster encounter
        for monster in monsters[:]:
            if player_instance.position == (monster.x, monster.y):
                print("A branch snaps nearby!")
                gameCombatLoop.fight_monster(player_instance, monster)
                monsters.remove(monster)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    # Assuming Player is initialized elsewhere and passed here
    explore_map(player_instance, monsters, player_move_counter)
