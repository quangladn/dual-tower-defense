import pygame
from threading import Thread
from time import sleep
from math import sqrt

from env import *

sizeGrid = 60


class Enemy:
    def __init__(self, route) -> None:
        self.x = 0
        self.y = 0

        self.health = 5
        self.max_health = self.health

        self.speed = 3
        self.idx = 0

        self.id = 0

        self.exited = False
        self.break_house = False
        self.damage = 5
        self.tick = 1
        self.route = route
        self.cash = 5
        self.summon()
        self.screen = None
        self.color = (100, 20, 20)
        self.isAttacked = False
        self.i_frame = True
        self.valuable = 0

        self.name = 0
        self.scale = 2

        Thread(target=self.remove_i_frame).start()

    def set_health(self, health, wave):
        extra_health = round(wave / 10) ** 2 * 2
        self.health = health + extra_health
        self.max_health = health + extra_health
        self.damage = self.health
        self.valuable = round(self.health / 10) + 2

    def remove_i_frame(self):
        sleep(0.05)
        self.i_frame = False

    def summon(self):
        col, row = self.route[self.idx]
        self.x = row * sizeGrid
        self.y = col * sizeGrid
        self.idx += 1
        self.Move()

    def Move_(self, posX, posY):
        self.speed = abs(round(self.speed))
        while (self.x != posX or self.y != posY) and self.health > 0:
            if self.x != posX:
                self.x += ((posX - self.x) / abs((posX - self.x))) * self.speed
                if abs((posX - self.x)) <= round(sqrt(self.speed)):
                    self.x = posX
            if self.y != posY:
                self.y += ((posY - self.y) / abs((posY - self.y))) * self.speed
                if abs((posY - self.y)) <= round(sqrt(self.speed)):
                    self.y = posY
            sleep(0.02)
        self.idx += 1
        try:
            col, row = self.route[self.idx]
            newX = row * sizeGrid
            newY = col * sizeGrid
            Thread(
                target=self.Move_,
                args=(
                    newX,
                    newY,
                ),
            ).start()
        except:
            if self.idx >= 54 and self.exited == False:
                self.break_house = True
                self.exited = True

    def Move(self):
        col, row = self.route[self.idx]
        newX = row * sizeGrid
        newY = col * sizeGrid
        Thread(
            target=self.Move_,
            args=(
                newX,
                newY,
            ),
        ).start()

    def set_model(self, name):
        self.name = name

    def load_model(self):
        model = pygame.Surface((sizeGrid, sizeGrid))
        if self.name == 0:
            return model
        try:
            model = pygame.image.load(
                ASSET_SOURCE + f"\\{self.name}.png"
            ).convert_alpha()
            model = pygame.transform.scale(
                model, (model.get_width() * self.scale, model.get_height() * self.scale)
            )
        except:
            pass
        return model

    def setTick(self, tick):
        self.tick = tick / 20

    def render(self, screen):
        # if self.name == 0:
        mx, my = pygame.mouse.get_pos()

        rect = pygame.Rect(self.x, self.y, sizeGrid, sizeGrid)
        # pygame.draw.rect(screen,(255,0,0),(self.x,self.y, 30,30), 2)
        hitbox = pygame.Rect(self.x + 8, self.y + 8, sizeGrid - 16, sizeGrid - 16)
        pygame.draw.rect(
            screen,
            self.color,
            hitbox,
        )

        model = self.load_model()
        model_rect = pygame.Rect(0, 0, model.get_width(), model.get_height())
        model_rect.center = hitbox.center
        model_rect.bottom = hitbox.bottom
        screen.blit(model, (model_rect.x, model_rect.y))
        if self.isAttacked == True:
            pygame.draw.rect(screen, (255, 40, 40), hitbox, 2)
        start_point = (20, 720 - 60 * 10 - 20)
        if rect.collidepoint(mx - start_point[0], my - start_point[1]):
            font = pygame.font.SysFont("", 30)
            text = font.render(
                f"{self.health}/{self.max_health}", True, (255, 255, 255)
            )
            r = text.get_rect()
            r.center = (mx - start_point[0], my - start_point[1] - 20)
            screen.blit(text, r.center)

    def take_damage(self, damage):
        if self.i_frame == True:
            return

        self.health -= damage
        if self.health <= 0:
            self.exited = True

    def update(self):
        if self.health <= 0:
            self.exited = True

    def get_center(self):
        rect = pygame.Rect(self.x + 8, self.y + 8, sizeGrid - 16, sizeGrid - 16)
        return rect.center

    def get_rect(self):
        rect = pygame.Rect(self.x + 8, self.y + 8, sizeGrid - 16, sizeGrid - 16)
        return rect
