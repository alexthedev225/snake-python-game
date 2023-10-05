import pygame
import random
import sys

pygame.init()

# Définir les constantes
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Définir les couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):
        self.body = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
        self.direction = pygame.Vector2(1, 0)
        self.new_segment = False

    def move(self):
        if self.new_segment:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_segment = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def change_direction(self, new_direction):
        if new_direction.x != -self.direction.x or new_direction.y != -self.direction.y:
            self.direction = new_direction

    def collide_with_wall(self):
        return self.body[0].x < 0 or self.body[0].x >= GRID_WIDTH or self.body[0].y < 0 or self.body[0].y >= GRID_HEIGHT

    def collide_with_self(self):
        return self.body[0] in self.body[1:]

    def get_head_position(self):
        return self.body[0]

class Food:
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self):
        self.position = pygame.Vector2(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Jouer", "Quitter"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Snake Game", True, BLACK)
        title_rect = title_text.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            text = font.render(option, True, GREEN if i == self.selected_option else BLACK)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)
            self.screen.blit(text, text_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Jouer
                        return "play"
                    elif self.selected_option == 1:  # Quitter
                        pygame.quit()
                        sys.exit()
        return None

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.score = 0
        self.main_menu = MainMenu(self.screen)

    def restart(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.score = 0

    def run(self):
        current_state = "menu"
        quit_game = False  # Ajoutez une variable pour gérer la sortie du jeu
        
        while True:
            if current_state == "menu":
                option = self.main_menu.handle_input()
                if option == "play":
                    current_state = "play"
                    self.restart()
                elif option is None:
                    self.main_menu.draw()
                    pygame.display.flip()
            elif current_state == "play":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction(pygame.Vector2(0, -1))
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(pygame.Vector2(0, 1))
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(pygame.Vector2(-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(pygame.Vector2(1, 0))
                        elif event.key == pygame.K_ESCAPE:
                            current_state = "menu"
                            self.main_menu.selected_option = 0
                        elif event.key == pygame.K_SPACE and self.game_over:
                            self.restart()
                            current_state = "play"

                if not self.game_over:
                    self.snake.move()
                    if self.snake.get_head_position() == self.food.position:
                        self.snake.new_segment = True
                        self.food.randomize_position()
                        self.score += 1

                    if self.snake.collide_with_wall() or self.snake.collide_with_self():
                        self.game_over = True

                self.screen.fill(WHITE)
                for segment in self.snake.body:
                    pygame.draw.rect(self.screen, GREEN, pygame.Rect(segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, RED, pygame.Rect(self.food.position.x * GRID_SIZE, self.food.position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Score: {self.score}", True, BLACK)
                score_rect = score_text.get_rect()
                score_rect.topleft = (10, 10)
                self.screen.blit(score_text, score_rect)

                if self.game_over:
                    game_over_font = pygame.font.Font(None, 70)
                    game_over_text = game_over_font.render("Game Over", True, RED)
                    game_over_rect = game_over_text.get_rect()
                    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90)
                    self.screen.blit(game_over_text, game_over_rect)

                    final_score_text = font.render(f"Score : {self.score}", True, BLACK)
                    final_score_rect = final_score_text.get_rect()
                    final_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 5)  # Ajustez la position en fonction de vos préférences
                    self.screen.blit(final_score_text, final_score_rect)

                    retry_text = font.render("Redémarrer", True, GREEN if self.main_menu.selected_option == 0 else BLACK)
                    retry_rect = retry_text.get_rect()
                    retry_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
                    self.screen.blit(retry_text, retry_rect)

                    quit_text = font.render("Quitter", True, GREEN if self.main_menu.selected_option == 1 else BLACK)
                    quit_rect = quit_text.get_rect()
                    quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)
                    self.screen.blit(quit_text, quit_rect)
                pygame.display.flip()

            if self.game_over:
                pygame.time.delay(100)  # Pause de 100 millisecondes pour ralentir la collecte des événements
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.main_menu.selected_option = (self.main_menu.selected_option - 1) % len(self.main_menu.options)
                        elif event.key == pygame.K_DOWN:
                            self.main_menu.selected_option = (self.main_menu.selected_option + 1) % len(self.main_menu.options)
                        elif event.key == pygame.K_RETURN:
                            if self.main_menu.selected_option == 0:  # Redémarrer
                                self.restart()
                                self.snake = Snake()
                                self.food = Food()
                                self.game_over = False
                                current_state = "play"
                            elif self.main_menu.selected_option == 1:  # Quitter
                               pygame.quit()
            self.clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    game = Game()
    game.run()
