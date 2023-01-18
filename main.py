import pygame

from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("material/Image/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        #pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Icon:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.icon = pygame.image.load("material/Image/mode_apple.jpg")
        self.x = 290
        self.y = 210

    def move_up(self):
        self.y -= 160
        self.draw()

    def move_down(self):
        self.y += 160
        self.draw()
        print(self.y)

    def draw(self):
        if self.y > 550:
            self.y = 210
        if self.y < 210:
            self.y = 550
            
        bg = pygame.image.load("material/Image/mode.jpg")
        self.parent_screen.blit(bg, (0, 0))
        self.parent_screen.blit(self.icon, (self.x, self.y))
        pygame.display.flip()


class snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("material/Image/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        #pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.icon = Icon(self.surface)
        self.icon.draw()

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("material/Music/Soundcrunch.wav")
        elif sound_name == "over":
            sound = pygame.mixer.Sound("material/Music/over.wav")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if (x1 >= x2) and x1 < x2 + SIZE:
            if (y1 >= y2) and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("material/Image/background.jpg")
        self.surface.blit(bg, (0, 0))

    def sc_background(self):
        bg = pygame.image.load("material/Image/sc.jpg")
        self.surface.blit(bg, (0, 0))

    def st_background(self):
        bg = pygame.image.load("material/Image/start_page.jpg")
        self.surface.blit(bg, (0, 0))

    def play_background_music(self):
        pygame.mixer.music.load('material/Music/music.wav')
        pygame.mixer.music.play(-1, 0)

    def mode_background(self):
        bg = pygame.image.load("material/Image/mode.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('crash')
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):

                raise "Collision Occurred"

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            raise "Hit the boundary error"

    def display_score(self):

        font = pygame.font.Font('material/Font/HocusPocusHollow.ttf', 35)
        score = font.render(f"Score : {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.sc_background()
        self.play_sound('over')
        font = pygame.font.Font('material/Font/HocusPocusHollow.ttf', 36)
        line1 = font.render(f"Game over ! Score : {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(line1, (195, 310))
        line2 = font.render("Retry press Enter  Quit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (195, 355))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        start = True
        menu = True
        speed = 0
        self.st_background()
        pygame.display.flip()

        while start:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        start = False
                elif event.type == QUIT:
                    return

        self.mode_background()
        pygame.display.flip()
        self.icon.draw()

        while menu:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.icon.move_up()
                    if event.key == K_DOWN:
                        self.icon.move_down()

                    if event.key == K_RETURN:
                        if self.icon.y == 210:
                            speed = 0.25
                            menu = False
                        elif self.icon.y == 370:
                            speed = 0.2
                            menu = False
                        elif self.icon.y == 530:
                            speed = 0.1
                            menu = False
                elif event.type == QUIT:
                    return

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(speed)


if __name__ == '__main__':
    game = Game()
    game.run()
