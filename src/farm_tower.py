import tower
import pygame
from threading import Thread
from time import sleep


class Tower_Farm(tower.Tower):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.damage = 10
        self.countdown_time = 2
        self.upgrade_list = [
            {"money": 5, "countdown": 0, "cost": 300},
            {"money": 10, "countdown": -0.5, "cost": 500},
            {"money": 25, "countdown": 0.5, "cost": 800},
            {"money": 50, "countdown": 0, "cost": 1000},
            {"money": 0, "countdown": -1, "cost": 1500},
        ]
        self.stat_show = {
            "money": self.damage,
            "countdown": self.countdown_time,
        }
        self.max_level = len(self.upgrade_list)
        self.cost = self.upgrade_list[0]["cost"]
        self.special_tower = 1
        self.color = (10, 150, 50)
        self.range_attack = 0
        self.price = 200

    def attack(self, enemys):
        if self.canAttack == False:
            return
        self.canAttack = False
        Thread(target=self.countdown_attack).start()
        return self.damage
