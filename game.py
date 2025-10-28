import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
            
        # Horizontal movement
        self.rect.x += self.vel_x
        
        # Check horizontal collisions
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hit_list:
            if self.vel_x > 0:
                self.rect.right = platform.rect.left
            elif self.vel_x < 0:
                self.rect.left = platform.rect.right
                
        # Vertical movement
        self.rect.y += self.vel_y
        
        # Check vertical collisions
        self.on_ground = False
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hit_list:
            if self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
                
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            
    def move_left(self):
        self.vel_x = -self.speed
        
    def move_right(self):
        self.vel_x = self.speed
        
    def stop(self):
        self.vel_x = 0

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.move_range = move_range
        self.vel_x = 2
        
    def update(self):
        self.rect.x += self.vel_x
        if self.rect.x >= self.start_x + self.move_range or self.rect.x <= self.start_x:
            self.vel_x *= -1

# Goal class
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Platformer Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_won = False
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goal_group = pygame.sprite.Group()
        
        # Create player
        self.player = Player(100, 400)
        self.all_sprites.add(self.player)
        
        # Create platforms
        self.create_level()
        
    def create_level(self):
        # Ground
        platform = Platform(0, 550, SCREEN_WIDTH, 50)
        self.platforms.add(platform)
        self.all_sprites.add(platform)
        
        # Platforms
        platforms_data = [
            (200, 450, 150, 20),
            (400, 350, 150, 20),
            (100, 250, 150, 20),
            (550, 250, 150, 20),
            (300, 150, 200, 20),
        ]
        
        for x, y, width, height in platforms_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
        # Create enemies
        enemy1 = Enemy(250, 420, 80)
        enemy2 = Enemy(450, 320, 100)
        self.enemies.add(enemy1, enemy2)
        self.all_sprites.add(enemy1, enemy2)
        
        # Create goal
        goal = Goal(350, 100)
        self.goal_group.add(goal)
        self.all_sprites.add(goal)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over and not self.game_won:
                        self.player.jump()
                elif event.key == pygame.K_r:
                    if self.game_over or self.game_won:
                        self.reset_game()
                        
    def update(self):
        if not self.game_over and not self.game_won:
            # Handle continuous key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
            else:
                self.player.stop()
                
            # Update sprites
            self.player.update(self.platforms)
            self.enemies.update()
            
            # Check collision with enemies
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.game_over = True
                
            # Check collision with goal
            if pygame.sprite.spritecollide(self.player, self.goal_group, False):
                self.game_won = True
                
            # Check if player falls off screen
            if self.player.rect.top > SCREEN_HEIGHT:
                self.game_over = True
                
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        
        # Draw text
        font = pygame.font.Font(None, 36)
        
        if self.game_over:
            text = font.render("Game Over! Press R to Restart", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
        elif self.game_won:
            text = font.render("You Win! Press R to Restart", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
        else:
            # Instructions
            instructions_font = pygame.font.Font(None, 24)
            instructions = [
                "Arrow Keys/A,D to Move",
                "Space to Jump",
                "Reach Yellow Goal!"
            ]
            for i, instruction in enumerate(instructions):
                text = instructions_font.render(instruction, True, BLACK)
                self.screen.blit(text, (10, 10 + i * 25))
        
        pygame.display.flip()
        
    def reset_game(self):
        self.game_over = False
        self.game_won = False
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.goal_group.empty()
        
        self.player = Player(100, 400)
        self.all_sprites.add(self.player)
        self.create_level()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Main entry point
if __name__ == "__main__":
    game = Game()
    game.run()
