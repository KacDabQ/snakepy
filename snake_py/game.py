import random
import pygame


class SnakePyGame:
    def __init__(self):
        self._initialize_pygame()
        self.running = True
        self.dt = 0
        self.snake_pos = [pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)]
        self.snake_dir = pygame.Vector2(1, 0)
        self.food_pos = self.get_random_food_position()
        self.score = 0

    def _initialize_pygame(self):
        '''
        Initialize pygame and joysticks.
        '''
        pygame.init()
        pygame.joystick.init()
        self.joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        print(self.joystick)
        self.screen = pygame.display.set_mode((800, 400))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

    def get_random_food_position(self):
        return pygame.Vector2(random.randint(0, self.screen.get_width() // 20) * 20,
                              random.randint(0, self.screen.get_height() // 20) * 20)

    def handle_events(self):
        new_events = pygame.event.get()
        for event in new_events:
            print(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.1:
                        self.snake_dir = pygame.Vector2(-1, 0)
                    elif event.value > 0.1:
                        self.snake_dir = pygame.Vector2(1, 0)
                if event.axis == 1:
                    if event.value < -0.1:
                        self.snake_dir = pygame.Vector2(0, -1)
                    elif event.value > 0.1:
                        self.snake_dir = pygame.Vector2(0, 1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake_dir != pygame.Vector2(0, 1):
            self.snake_dir = pygame.Vector2(0, -1)
        if keys[pygame.K_DOWN] and self.snake_dir != pygame.Vector2(0, -1):
            self.snake_dir = pygame.Vector2(0, 1)
        if keys[pygame.K_LEFT] and self.snake_dir != pygame.Vector2(1, 0):
            self.snake_dir = pygame.Vector2(-1, 0)
        if keys[pygame.K_RIGHT] and self.snake_dir != pygame.Vector2(-1, 0):
            self.snake_dir = pygame.Vector2(1, 0)

    def update_snake(self):
        new_head = self.snake_pos[0] + self.snake_dir * 20
        self.snake_pos = [new_head] + self.snake_pos[:-1]

        # Check for collision with boundaries
        if (new_head.x < 0 or new_head.x >= self.screen.get_width() or
                new_head.y < 0 or new_head.y >= self.screen.get_height()):
            self.running = False

        # Check for collision with itself
        if (new_head in self.snake_pos[1:]):
            self.running = False

        # Check for collision with food
        if new_head == self.food_pos:
            self.snake_pos.append(self.snake_pos[-1])
            self.food_pos = self.get_random_food_position()
            self.score += 1


    def run(self):
        while self.running:
            # Handle events captured by pygame
            self.handle_events()

            # Run game logic
            self.update_snake()

            # Draw game
            self.screen.fill("black")
            for pos in self.snake_pos:
                pygame.draw.rect(self.screen, "green", pygame.Rect(pos.x, pos.y, 20, 20))
            pygame.draw.rect(self.screen, "red", pygame.Rect(self.food_pos.x, self.food_pos.y, 20, 20))

            pygame.display.flip()
            self.dt = self.clock.tick(10) / 1000

        print(f"Game Over! Your score: {self.score}")