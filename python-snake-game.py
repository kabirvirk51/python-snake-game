import pygame
import sys
import time
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        # Initialize game variables
        self.difficulty = 25
        self.frame_size_x = 720
        self.frame_size_y = 480
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        pygame.display.set_caption('Snake Eater')
        self.fps_controller = pygame.time.Clock()

        # Colors
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'white': pygame.Color(255, 255, 255),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0),
            'blue': pygame.Color(0, 0, 255)
        }

        # Initial snake position and body
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        # Initial food position and spawn status
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True

        # Initial snake direction and change direction
        self.direction = 'RIGHT'
        self.change_to = self.direction

        # Initial score
        self.score = 0

    def run(self):
        # Main game loop
        while True:
            self.handle_events()
            self.change_direction()
            self.move_snake()
            self.grow_snake()
            self.spawn_food()
            self.update_graphics()
            self.check_game_over()

            pygame.display.update()
            self.fps_controller.tick(self.difficulty)

    def handle_events(self):
        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event.key)

    def handle_key_event(self, key):
        # Handle key events for snake direction and game control
        if key == pygame.K_UP or key == ord('w'):
            self.change_to = 'UP'
        if key == pygame.K_DOWN or key == ord('s'):
            self.change_to = 'DOWN'
        if key == pygame.K_LEFT or key == ord('a'):
            self.change_to = 'LEFT'
        if key == pygame.K_RIGHT or key == ord('d'):
            self.change_to = 'RIGHT'
        if key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def change_direction(self):
        # Change the direction of the snake
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move_snake(self):
        # Move the snake based on its direction
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def grow_snake(self):
        # Make the snake grow and handle food consumption
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

    def spawn_food(self):
        # Spawn food at a random position
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                             random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True

    def update_graphics(self):
        # Update the game graphics
        self.game_window.fill(self.colors['black'])
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.colors['green'], pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.game_window, self.colors['white'], pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        self.show_score(1, self.colors['white'], 'consolas', 20)

    def check_game_over(self):
        # Check game over conditions
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
            self.game_over()
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over()

    def game_over(self):
        # Handle game over screen
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, self.colors['red'])
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(self.colors['black'])
        self.game_window.blit(game_over_surface, game_over_rect)

        try_again_font = pygame.font.SysFont('times new roman', 40)
        try_again_surface = try_again_font.render('Try Again', True, self.colors['white'])
        try_again_rect = try_again_surface.get_rect()
        try_again_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.5)
        self.game_window.blit(try_again_surface, try_again_rect)
        self.show_score(0, self.colors['red'], 'times new roman', 20)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_rect.collidepoint(pygame.mouse.get_pos()):
                        self.__init__()  # Restart the game

    def show_score(self, choice, color, font, size):
        # Display the game score
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
