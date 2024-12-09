import pygame
import random

pygame.init()

# Window settings
window_x = 1200
window_y = 800
screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Running for Living")

# Colors
SKY_COLOR = (135, 206, 235)
GROUND_COLOR1 = (139, 69, 19)
GROUND_COLOR2 = (160, 82, 45)
GROUND_COLOR3 = (205, 133, 63)
GRASS_COLOR = (34, 139, 34)  # Green for the grass

# Icon
icon = pygame.image.load("cat2.png")
pygame.display.set_icon(icon)

# Mouse Runner
mouse_xsize = 100
mouse_ysize = 100
mouse_speed = 10

mouse_run1 = pygame.image.load("mouse1.png")
mouse_run1 = pygame.transform.scale(mouse_run1, (mouse_xsize, mouse_ysize))
mouse_run2 = pygame.image.load("mouse2.png")
mouse_run2 = pygame.transform.scale(mouse_run2, (mouse_xsize, mouse_ysize))

mouse_images = [mouse_run1, mouse_run2]
mouse_x = 300
mouse_y = 580
mouse_jump = False
mouse_jump_height = 60
mouse_jump_speed = 10
jump_offset = 0
gravity = 5

# Cat
cat_xsize = 150
cat_ysize = 150

cat_run1 = pygame.image.load("cat1.png")
cat_run1 = pygame.transform.scale(cat_run1, (cat_xsize, cat_ysize))
cat_run2 = pygame.image.load("cat2.png")
cat_run2 = pygame.transform.scale(cat_run2, (cat_xsize, cat_ysize))

cat_images = [cat_run1, cat_run2]
cat_x = -150
cat_y = 580
cat_move = False

# Trees and Clouds
tree_images = [
    pygame.image.load("tree1.png"),
    pygame.image.load("tree2.png"),
    pygame.image.load("tree3.png"),
    pygame.image.load("tree4.png"),
]
tree_positions = [(random.randint(0, window_x), 450) for _ in range(4)]

cloud_images = [
    pygame.image.load("cloud1.png"),
    pygame.image.load("cloud2.png"),
]
cloud_positions = [(random.randint(0, window_x), random.randint(50, 200)) for _ in range(2)]

# Scale tree and cloud images
tree_images = [pygame.transform.scale(tree, (100, 150)) for tree in tree_images]
cloud_images = [pygame.transform.scale(cloud, (150, 100)) for cloud in cloud_images]

# Stones
stone_size = 50
stone_img = pygame.image.load("stone.png")
stone_img = pygame.transform.scale(stone_img, (stone_size, stone_size))
stones = [{"x": random.randint(400, window_x), "y": 640}]

# Bird
bird_images = [
    pygame.image.load("1.png"),
    pygame.image.load("2.png"),
    pygame.image.load("3.png"),
    pygame.image.load("4.png"),
    pygame.image.load("5.png"),
]
bird_images = [pygame.transform.scale(bird, (50, 50)) for bird in bird_images]
bird_x = window_x
bird_y = random.randint(100, 400)
bird_speed = 6  # The speed of the bird's movement (adjust as needed)

# Ground scroll
ground_scroll_speed = 5
ground_x_offset = 0

# Game Variables
clock = pygame.time.Clock()
run_game = True
game_over = False
current_image_index = 0
image_display_time = 100  # Time in milliseconds for image switch speed
last_image_switch_time = pygame.time.get_ticks()

# Timer for the score (how many seconds the mouse has survived)
start_time = pygame.time.get_ticks()

# Game Over Timer
game_over_start_time = 0
game_over_duration = 4000  # 1 second (adjust as needed)

# Functions
def draw_background():
    # Draw sky
    screen.fill(SKY_COLOR)

    # Draw trees
    for i, (x, y) in enumerate(tree_positions):
        tree_positions[i] = (x - ground_scroll_speed, y)
        if tree_positions[i][0] < -100:  # Tree goes off-screen
            tree_positions[i] = (window_x + random.randint(0, 200), y)
        screen.blit(tree_images[i % len(tree_images)], (x, y))

    # Draw grass above the ground
    pygame.draw.rect(screen, GRASS_COLOR, (0, 600 - 30, window_x, 30))  # Green grass layer

    # Draw ground
    global ground_x_offset
    ground_x_offset -= ground_scroll_speed
    if ground_x_offset <= -window_x:
        ground_x_offset = 0

    pygame.draw.rect(screen, GROUND_COLOR1, (ground_x_offset, 600, window_x * 2, 50))
    pygame.draw.rect(screen, GROUND_COLOR2, (ground_x_offset, 650, window_x * 2, 50))
    pygame.draw.rect(screen, GROUND_COLOR3, (ground_x_offset, 700, window_x * 2, 100))

    # Draw sand/stones
    draw_sand()

def draw_sand():
    # Randomly place small stones (or sand grains) on the ground
    for _ in range(150):  # Adjust the range to control the density of the sand/stones
        x = random.randint(0, window_x)
        y = random.randint(600, 700)  # Position it between ground and sand area
        size = random.randint(1, 3)  # Small size for stones/sand particles
        color = (random.randint(150, 200), random.randint(120, 150), random.randint(80, 100))  # Earthy color
        pygame.draw.circle(screen, color, (x, y), size)

def draw_mouse(x, y, image):
    screen.blit(image, (x, y))

def draw_cat(x, y, image):
    screen.blit(image, (x, y))

def draw_stones():
    for stone in stones:
        stone["x"] -= ground_scroll_speed
        if stone["x"] < -50:
            stone["x"] = random.randint(window_x, window_x + 500)
        screen.blit(stone_img, (stone["x"], stone["y"]))

def draw_bird(x, y, image):
    screen.blit(image, (x, y))

def check_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    return (obj1_x < obj2_x + obj2_width and
            obj1_x + obj1_width > obj2_x and
            obj1_y < obj2_y + obj2_height and
            obj1_y + obj1_height > obj2_y)

def draw_score(score):
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White color
    screen.blit(score_text, (window_x - 150, 20))

def draw_game_over():
    font = pygame.font.SysFont("Arial", 80)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Red color
    screen.blit(game_over_text, (window_x // 3, window_y // 3))

# Main game loop
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    # Keyboard input for mouse movement
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and mouse_x > 0:
            mouse_x -= mouse_speed
        if keys[pygame.K_RIGHT] and mouse_x + mouse_xsize < window_x:
            mouse_x += mouse_speed

        # Jump logic
        if not mouse_jump and keys[pygame.K_SPACE]:
            mouse_jump = True
            jump_offset = -mouse_jump_height
        if mouse_jump:
            mouse_y += jump_offset
            jump_offset += gravity
            if mouse_y >= 580:
                mouse_y = 580
                mouse_jump = False

    # Background and track
    draw_background()

    # Update the mouse image every `image_display_time` milliseconds for fast animation
    if pygame.time.get_ticks() - last_image_switch_time >= image_display_time:
        current_image_index = (current_image_index + 1) % len(mouse_images)  # Modulo operation to stay within bounds
        last_image_switch_time = pygame.time.get_ticks()

    # Draw the mouse with alternating images
    draw_mouse(mouse_x, mouse_y, mouse_images[current_image_index])

    # Draw the bird
    bird_x -= bird_speed  # Move the bird from right to left
    if bird_x < -50:  # If the bird goes off-screen, reset its position
        bird_x = window_x
        bird_y = random.randint(100, 400)

    current_bird_image = bird_images[(pygame.time.get_ticks() // 100) % len(bird_images)]  # Change bird image based on time
    draw_bird(bird_x, bird_y, current_bird_image)

    # Cat movement after game over
    if cat_move:  # Move the cat only if cat_move is True
        if cat_x < mouse_x:
            cat_x += 5
        elif cat_x > mouse_x:
            cat_x -= 5

    # Display the cat
    draw_cat(cat_x, cat_y, cat_images[current_image_index])

    # Stones
    if not game_over:
        draw_stones()

    # Collision detection
    if not game_over:
        for stone in stones:
            if check_collision(mouse_x, mouse_y, mouse_xsize, mouse_ysize,
                               stone["x"], stone["y"], stone_size, stone_size):
                print("Game Over: Hit a stone!")
                game_over = True
                cat_move = True  # Start moving the cat immediately after stone hit
                game_over_start_time = pygame.time.get_ticks()  # Record the time when game over happens
                break

    # Stop the game when the cat "catches" the mouse
    if not game_over and cat_x >= mouse_x:
        print("Game Over: The cat caught the mouse!")
        game_over = True
        game_over_start_time = pygame.time.get_ticks()  # Record the time when game over happens
        cat_move = True  # Start moving the cat immediately when the mouse is caught

    # Game over sequence
    if game_over:
        # Display "Game Over" for 1 second after the cat reaches the mouse or hits the stone
        if pygame.time.get_ticks() - game_over_start_time < game_over_duration:
            draw_game_over()
        else:
            # After 1 second, stop the game
            run_game = False  # End the game after the "Game Over" screen is shown

    # Display the current score (time survived)
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds
        draw_score(elapsed_time)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
