import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 10

# Snake class
class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def check_collision(self):
        head = self.body[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or 
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def spawn(self):
        self.position = self.random_position()

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Game class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, GRID_SIZE):
                    self.snake.direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -GRID_SIZE):
                    self.snake.direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and self.snake.direction != (GRID_SIZE, 0):
                    self.snake.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-GRID_SIZE, 0):
                    self.snake.direction = (GRID_SIZE, 0)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()
        
        return True

    def update(self):
        if not self.game_over:
            self.snake.move()
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.spawn()
                self.score += 10
            
            # Check collision
            if self.snake.check_collision():
                self.game_over = True

    def draw(self):
        screen.fill(BLACK)
        
        self.snake.draw(screen)
        self.food.draw(screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Press SPACE to restart", True, YELLOW)
            
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()

# Main game loop

def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()