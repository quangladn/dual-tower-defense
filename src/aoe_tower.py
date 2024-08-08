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
            {"damage": 3, "countdown": 1, "range": 150},
        )
        self.upgrade_list = [
            {"damage": 2, "countdown": 0, "range": 50, "cost": 300},
            {"damage": 3, "countdown": -0.2, "range": 0, "cost": 500},
            {"damage": 5, "countdown": -0.05, "range": 50, "cost": 800},
            {"damage": 10, "countdown": 0, "range": 0, "cost": 1000},
            {"damage": -10, "countdown": -0.5, "range": 0, "cost": 1500},
        ]
        self.max_level = len(self.upgrade_list)
        self.cost = self.upgrade_list[0]["cost"]
        self.color = (200, 200, 0)
        self.price = 250

    def render(self, screen):
        super().render(screen)

    def attack_t(self, enemys):
        attacked_enemy = 0
        for enemy in enemys:
            if (
                self.get_distance(enemy) < self.range_attack
                and attacked_enemy < self.max_enemy
            ):
                enemy.isAttacked = True
                enemy.take_damage(self.damage)
                attacked_enemy += 1
            elif attacked_enemy >= self.max_enemy:
                break
        if attacked_enemy > 0:
            self.canAttack = False
            Thread(target=self.countdown_attack).start()

    def attack(self, enemys):
        if self.canAttack == False:
            return
        Thread(target=self.attack_t, args=(enemys,)).start()
        return 0
