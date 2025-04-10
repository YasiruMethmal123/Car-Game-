import random
from time import sleep

import pygame
from pathlib2 import Path

class CarRace:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):
        self.crashed = False

        # Load car image (assuming it's in the same directory as the script)
        self.carImg = pygame.image.load(self.root_path + "/Assets/car.png")
        self.car_x_cordinate = (self.display_width * 0.45)
        self.car_y_cordinate = (self.display_height * 0.8)
        self.car_width = 49

        # Load enemy car 1 image
        self.enemy_car = pygame.image.load(self.root_path + "/Assets/enemy_car_1.png")
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Load enemy car 2 image (replace with the new blue car)
        self.enemy_car_two = pygame.image.load(self.root_path + "/Assets/enemy_car_2.png")  # Save the blue car image as "blue_car.png"
        self.enemy_car_startx_two = random.randrange(310, 450)
        self.enemy_car_starty_two = -600
        self.enemy_car_speed_two = 5
        self.enemy_car_width_two = 49  # Adjust if the blue car's width is different
        self.enemy_car_height_two = 100  # Adjust if the blue car's height is different

        # Load background image
        self.bgImg = pygame.image.load(self.root_path + "/Assets/road.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race --Yasiru')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.crashed = True
                    elif event.key == pygame.K_LEFT:
                        self.car_x_cordinate = max(0, self.car_x_cordinate - 50)  # Clamp to left edge
                        print("CAR X COORDINATES: %s" % self.car_x_cordinate)
                    elif event.key == pygame.K_RIGHT:
                        self.car_x_cordinate = min(self.display_width - self.car_width,
                                                   self.car_x_cordinate + 50)  # Clamp to right edge
                        print("CAR X COORDINATES: %s" % self.car_x_cordinate)
                    print("x: {x}, y: {y}".format(x=self.car_x_cordinate, y=self.car_y_cordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            # Enemy car 1
            self.run_enemy_car(self.enemy_car, self.enemy_car_startx, self.enemy_car_starty)  # Pass the correct image
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(220, 531)

            # Enemy car 2 (now the blue car)
            self.run_enemy_car(self.enemy_car_two, self.enemy_car_startx_two, self.enemy_car_starty_two)  # Pass the correct image
            self.enemy_car_starty_two += self.enemy_car_speed_two

            if self.enemy_car_starty_two > self.display_height:
                self.enemy_car_starty_two = 0 - self.enemy_car_height_two
                self.enemy_car_startx_two = random.randrange(220, 531)

            self.car(self.car_x_cordinate, self.car_y_cordinate)
            self.highscore(self.count)
            self.count += 1

            if self.count % 100 == 0:
                self.enemy_car_speed += 1
                self.enemy_car_speed_two += 1
                self.bg_speed += 1

            # Collision check for enemy car 1
            if self.car_y_cordinate < self.enemy_car_starty + self.enemy_car_height and self.enemy_car_starty + self.enemy_car_height > self.car_y_cordinate:
                if (
                        self.car_x_cordinate > self.enemy_car_startx and self.car_x_cordinate < self.enemy_car_startx + self.enemy_car_width) or \
                        (
                                self.car_x_cordinate + self.car_width > self.enemy_car_startx and self.car_x_cordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width):
                    self.crashed = True
                    self.display_message("Game Over !")

            # Collision check for enemy car 2
            if self.car_y_cordinate < self.enemy_car_starty_two + self.enemy_car_height_two and self.enemy_car_starty_two + self.enemy_car_height_two > self.car_y_cordinate:
                if (
                        self.car_x_cordinate > self.enemy_car_startx_two and self.car_x_cordinate < self.enemy_car_startx_two + self.enemy_car_width_two) or \
                        (
                                self.car_x_cordinate + self.car_width > self.enemy_car_startx_two and self.car_x_cordinate + self.car_width < self.enemy_car_startx_two + self.enemy_car_width_two):
                    self.crashed = True
                    self.display_message("Game Over !")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, car_image, thingx, thingy):  # Modified to accept the car image as a parameter
        self.gameDisplay.blit(car_image, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

if __name__ == '__main__':
    car_racing = CarRace()
    car_racing.racing_window()