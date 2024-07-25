import pygame
from threading import Thread
from time import sleep
from math import sqrt

TARGET_FIRST = 1
TARGET_LAST = 2

START_POINT = (20, 720 - 60 * 10 - 20)


class Tower:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.w = 40
        self.h = 40

        self.speed = 3

        self.canAttack = True
        self.color = (100, 100, 255)

        self.damage = 3
        self.countdown_time = 0.5
        self.range_attack = 180
        self.self_hitbox = pygame.Rect(self.x, self.y, self.w, self.h)
        self.self_hitbox.center = (self.x, self.y)

        self.target = TARGET_FIRST
        self.level = 1
        self.upgrade_list = [
            {"damage": 2, "countdown": -0, "range": 5, "cost": 100},
            {"damage": 2, "countdown": -0.25, "range": 10, "cost": 150},
            {"damage": 10, "countdown": +0.2, "range": 10, "cost": 200},
        ]
        self.cost = self.upgrade_list[0]["cost"]

        self.stat_show = {
            "damage": self.damage,
            "countdown": self.countdown_time,
            "range": self.range_attack,
        }
        self.max_level = len(self.upgrade_list) + 1
        self.price = 100
        # Thread(target=self.countdown_attack).start()

    def get_distance(self, enemy):
        x, y = self.self_hitbox.center
        ex, ey = enemy.get_center()

        a = ex - x
        b = ey - y

        distance = sqrt((a**2 + b**2))
        return distance

    def countdown_attack(self):
        sleep(self.countdown_time)
        self.canAttack = True

    def attack(self, enemys):
        if self.canAttack == False:
            return
        for enemy in enemys:
            if self.get_distance(enemy) < self.range_attack and self.canAttack == True:
                enemy.isAttacked = True
                enemy.take_damage(self.damage)
                self.canAttack = False
                Thread(target=self.countdown_attack).start()
                return 1
            # print(22)

    def check_collide(self, player):
        local_rect = pygame.Rect(
            self.x + START_POINT[0], self.y + START_POINT[1], self.w, self.h
        )
        local_rect.center = (self.x + START_POINT[0], self.y + START_POINT[1])

        if local_rect.colliderect(player.get_rect()):
            return True
        return False

    def render(self, screen):
        mx, my = pygame.mouse.get_pos()

        pygame.draw.rect(screen, self.color, self.self_hitbox)
        if self.self_hitbox.collidepoint(mx - START_POINT[0], my - START_POINT[1]):
            pygame.draw.circle(
                screen, (255, 255, 255), self.self_hitbox.center, self.range_attack, 3
            )

    def update_show_stat(self, stat):
        for k in self.stat_show.keys():
            self.stat_show[k] += stat[k]

    def upgrade(self, money):
        if self.level >= self.max_level:
            return 0
        stat = self.upgrade_list[self.level - 1]
        if money < stat["cost"]:
            return 0
        self.damage += stat["damage"]
        self.countdown_time += stat["countdown"]
        self.range_attack += stat["range"]
        self.update_show_stat(stat)
        try:
            self.cost = self.upgrade_list[self.level]["cost"]
        except IndexError:
            self.cost = "MAXED"
        self.level += 1

        return stat["cost"]

    def get_rect(self):
        return self.self_hitbox
