
import pygame
import numpy as np
from bayesOpt import *
from food import Food
from game import Game

class Player(object):
    def __init__(self, size: list[list]):
        x = 0.45 * size[0]
        y = 0.5 * size[1]
        self.x = x - x % 20
        self.y = y - y % 20
        self.tail = []
        self.tail.append(self.position)
        self.food = 1
        self.eaten = False
        self.image = pygame.image.load('img/snakeBody.png')
        self.x_change = 20
        self.y_change = 0

    @property
    def position(self):
        return [self.x, self.y]

    def update_position(self):
        if self.tail[-1] == self.position: 
            return
        for i in range(max(0, self.food - 1)):
            self.tail[i] = self.tail[i + 1]
        self.tail[-1] = self.position

    def do_move(self, move, x: float, y: float, game: Game, food: Food):
        move_array = [self.x_change, self.y_change]

        if self.eaten:
            self.tail.append([self.x, self.y])
            self.eaten = False
            self.food += 1
        if np.array_equal(move, [1, 0, 0]):
            move_array = self.x_change, self.y_change
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # right - going horizontal
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            move_array = [self.y_change, 0]
        self.x_change, self.y_change = move_array
        self.x, self.y = x + self.x_change, y + self.y_change

        if self.x < 20 or self.x > game.game_width - 40 \
                or self.y < 20 \
                or self.y > game.game_height - 40 \
                or [self.x, self.y] in self.tail:
            game.crash = True
        self.eat(food, game)

        self.update_position()

    def eat(self, food: Food, game: Game):
        if self.position == food.position:
            food.randomize(game.size, self.tail)
            self.eaten = True
            game.score += 1

    def display_player(self, food: Food, game: Game):
        if game.crash == False:
            for i in range(food):
                x_temp, y_temp = self.tail[len(self.tail) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))
        else:
            pygame.time.wait(300)