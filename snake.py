import pygame
import random

# Inicialização do pygame
pygame.init()

# Configurações do jogo
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
SNAKE_SPEED = 10

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicialização da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Classe Snake
class Snake:
    def __init__(self):
        self.positions = [(5, 5)]
        self.direction = (1, 0)
    
    def update(self, eat_food):
        new_head = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])
        self.positions.insert(0, new_head)
        
        if not eat_food:
            self.positions.pop()
    
    def change_direction(self, new_direction):
        if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    def get_head_position(self):
        return self.positions[0]

    def collide_with_boundaries(self):
        head_x, head_y = self.get_head_position()
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT

    def collide_with_self(self):
        return self.get_head_position() in self.positions[1:]

# Classe Food
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            self.is_food_on_screen = True
    
    def set_food_off_screen(self):
        self.is_food_on_screen = False

# Função principal
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        
        snake.update(False)
        if snake.get_head_position() == food.position:
            snake.update(True)
            food.set_food_off_screen()
            score += 1
        
        if snake.collide_with_boundaries() or snake.collide_with_self():
            pygame.quit()
            return
        
        food.spawn_food()
        
        screen.fill(BLACK)
        for segment in snake.positions:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, RED, pygame.Rect(food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Renderizar a pontuação na tela
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
