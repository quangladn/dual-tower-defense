import tower
import pygame
from threading import Thread
from time import sleep
from math import degrees, radians, sin, cos, pi, atan2


class Tower_Piercing(tower.Tower):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.set_stat(
            {"damage": 5, "countdown": 0.5, "range": 300},
        )
        self.angle = (0, 0)
        self.D_hitbox = (0, 0, 0, 0)
        self.color = (100, 255, 100)
        self.price = 350

    def render(self, screen):
        super().render(screen)

    def attack(self, enemys):
        if self.canAttack == False:
            return
        attacked_enemy = 0
        for enemy in enemys:
            if self.get_distance(enemy) < self.range_attack:
                if attacked_enemy <= 0:
                    self.D_hitbox = (
                        self.get_rect().centerx,
                        self.get_rect().centery,
                        enemy.get_center()[0],
                        enemy.get_center()[1],
                    )
                    self.angle = (
                        enemy.get_center()[0] - self.get_rect().centerx,
                        enemy.get_center()[1] - self.get_rect().centery,
                    )
                    enemy.isAttacked = True
                    attacked_enemy += 1
                    enemy.take_damage(self.damage)
                elif attacked_enemy > 0:
                    if enemy.get_rect().clipline(
                        (
                            (self.x, self.y),
                            (
                                self.x + self.angle[0] * self.range_attack,
                                self.y + self.angle[1] * self.range_attack,
                            ),
                        )
                    ):
                        enemy.isAttacked = True
                        attacked_enemy += 1
                        enemy.take_damage(self.damage)

        self.canAttack = False
        Thread(target=self.countdown_attack).start()
        return 0
