import tower
import pygame
from threading import Thread
from time import sleep
from math import sqrt, sin, cos, pi


class Tower_AOE(tower.Tower):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.max_enemy = 10
        self.set_stat(
            {"damage": 2, "countdown": 0.5, "range": 150},
        )
        self.color = (200, 200, 0)

    def render(self, screen):
        super().render(screen)

    def attack(self, enemys):
        if self.canAttack == False:
            return
        attacked_enemy = 0
        for enemy in enemys:
            if (
                self.get_distance(enemy) < self.range_attack
                and attacked_enemy < self.max_enemy
            ):
                enemy.isAttacked = True
                enemy.take_damage(self.damage)
            elif attacked_enemy >= self.max_enemy:
                break

        self.canAttack = False
        Thread(target=self.countdown_attack).start()
