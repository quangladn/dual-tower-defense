import socket
import pickle
import pygame
import os
from _thread import *
from threading import Thread
from time import sleep
from copy import copy
from player import Player
from enemy import Enemy
from tower import Tower
from env import *

dev_mode = True
HOST_PLAYER = 0

server = SERVER
port = PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

player_1 = Player(200, 100, (255, 0, 0))
player_2 = Player(100, 100, (0, 0, 255))

map_game = [
    [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
    [-2, 45, 44, 43, 42, 41, -2, 21, 20, 19, 18, -2, 0, -1],
    [-2, 46, -2, -2, -2, 40, -2, 22, -2, -2, 17, -2, 1, -2],
    [-2, 47, -2, -2, -2, 39, -2, 23, -2, -2, 16, -2, 2, -2],
    [-2, 48, -2, 36, 37, 38, -2, 24, -2, -2, 15, -2, 3, -2],
    [-2, 49, -2, 35, -2, -2, -2, 25, -2, 13, 14, -2, 4, -2],
    [-2, 50, -2, 34, -2, -2, -2, 26, -2, 12, -2, -2, 5, -2],
    [-2, 51, -2, 33, -2, -2, -2, 27, -2, 11, -2, -2, 6, -2],
    [53, 52, -2, 32, 31, 30, 29, 28, -2, 10, 9, 8, 7, -2],
    [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
]
route = []
for i in range(-1, 54):
    for col in range(10):
        for row in range(14):
            if map_game[col][row] == i:
                route.append((col, row))
wave = 1
wave_design = [
    {
        "wave": 1,
        "enemy": {"mini": [10, 0.35]},
    },
    {
        "wave": 2,
        "enemy": {
            "mini": [15, 0.35],
            "basic": [15, 0.55],
        },
    },
    {
        "wave": 3,
        "enemy": {"basic": [30, 0.55], "large": [3, 0.8]},
    },
    {
        "wave": 4,
        "enemy": {"mini": [30, 0.35], "basic": [30, 0.55], "large": [10, 0.8]},
    },
    {
        "wave": 5,
        "enemy": {
            "mini": [10, 0.35],
            "basic": [50, 0.55],
            "large": [10, 0.8],
            "small_titan": [1, 1],
            "over_speed": [1, 1],
        },
    },
    {
        "wave": 6,
        "enemy": {"basic": [10, 0.55], "large": [30, 0.8], "small_titan": [10, 1]},
    },
    {
        "wave": 7,
        "enemy": {"large": [30, 0.8], "small_titan": [10, 1]},
    },
    {
        "wave": 8,
        "enemy": {"large": [40, 0.8], "small_titan": [12, 1]},
    },
    {
        "wave": 9,
        "enemy": {
            "large": [35, 0.8],
            "small_titan": [15, 1],
        },
    },
    {
        "wave": 10,
        "enemy": {"large": [50, 0.8], "small_titan": [30, 1], "basic_captain": [3, 1]},
    },
    {
        "wave": 11,
        "enemy": {"small_titan": [50, 1], "basic_captain": [5, 1]},
    },
    {
        "wave": 12,
        "enemy": {"small_titan": [80, 0.8], "basic_captain": [10, 1]},
    },
    {
        "wave": 13,
        "enemy": {"small_titan": [100, 0.8], "basic_captain": [30, 1]},
    },
    {
        "wave": 14,
        "enemy": {"large": [50, 0.8], "small_titan": [80, 1], "basic_captain": [50, 1]},
    },
    {
        "wave": 15,
        "enemy": {"basic_captain": [50, 1], "knight": [5, 2]},
    },
]
can_spawn_wave = True

house_health = 100
max_house_health = 100

players = [player_1, player_2]
new_enemy = Enemy(route)
enemys = []
towers = [Tower(690, 310)]
towers = []

money = 200

currentPlayer = 0
disconnected = 0

pygame.init()


def spawn_wave(wave_design: dict):
    global enemys, can_spawn_wave, wave
    can_spawn_wave = False
    for k in wave_design.keys():
        time_spawn = wave_design[k][0]
        delay_time = wave_design[k][1] - 0.2
        # delay_time = 0.02
        if k == "mini":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.set_health(1, wave)
                enemy.speed = 5
                enemy.color = (20, 50, 20)
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "basic":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.set_health(8, wave)
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "large":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.color = (100, 20, 100)
                enemy.set_health(24, wave)
                enemy.speed = 2
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "small_titan":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.color = (255, 100, 20)
                enemy.set_health(50, wave)
                enemy.speed = 2
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "basic_captain":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.color = (200, 200, 20)
                enemy.set_health(65, wave)
                enemy.speed = 4
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "over_speed":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.color = (200, 200, 255)
                enemy.set_health(15, wave)
                enemy.speed = 20
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
        elif k == "knight":
            for i in range(time_spawn):
                enemy = Enemy(route)
                enemy.color = (200, 200, 255)
                enemy.set_health(100, wave)
                enemy.speed = 7
                enemy.set_model(k)
                enemys.append(enemy)
                sleep(delay_time)
    while len(enemys) > 0:
        sleep(0)
    sleep(3)
    can_spawn_wave = True
    wave += 1


def threaded_client(conn, player_idx):
    global disconnected, HOST_PLAYER, enemys, can_spawn_wave, house_health, money
    conn.send(pickle.dumps([players[player_idx], map_game, max_house_health]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(BUFSIZE))
            players[player_idx] = data

            if not data:
                print("Disconnected")
                break
            else:
                towers.extend(players[0].towers)
                for t in players[0].upgrade_towers:
                    money -= towers[t].upgrade(money)

                towers.extend(players[1].towers)
                for t in players[1].upgrade_towers:
                    money -= towers[t].upgrade(money)

                if can_spawn_wave == True:
                    for w in wave_design:
                        if w["wave"] >= wave:
                            Thread(target=spawn_wave, args=(w["enemy"],)).start()
                            break

                for tower in towers:
                    if tower.price != -1:
                        if money < tower.price:
                            towers.remove(tower)
                        else:
                            money -= tower.price
                            tower.price = -1
                    if tower.canAttack == False:
                        continue
                    tower.attack(enemys)

                for enemy in enemys:
                    enemy.update()
                    if enemy.exited == True:
                        money += enemy.valuable
                        enemys.remove(enemy)
                        if enemy.break_house == True:
                            house_health -= enemy.damage

                if player_idx == HOST_PLAYER:
                    players[1].health = house_health
                    reply = [players[1], enemys, towers, wave, money]
                    print(123)
                else:
                    players[0].health = house_health
                    reply = [players[0], enemys, towers, wave, money]
                    print(123)
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()
    os._exit(0)
    if dev_mode == True:
        disconnected += 1
        if disconnected == 2:
            os._exit(0)


def run():
    global currentPlayer
    while True:
        conn, addr = s.accept()
        # print("CurrentPlayer: ",currentPlayer, end="\r")
        # print("Connected to:", addr)
        # print(disconnected)

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


run()
