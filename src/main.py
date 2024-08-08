import pygame
import os
from player import Player
from network import Network
from tower import Tower
from aoe_tower import Tower_AOE
from farm_tower import Tower_Farm
from piercing_tower import Tower_Piercing
from env import *

pygame.init()

G_SIZE_SCREEN = (1280, 720)
G_FPS = 60
L_run = True
G_screen = pygame.display.set_mode(
    G_SIZE_SCREEN, pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF, 16
)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

G_clock = pygame.time.Clock()

font_s20 = pygame.font.SysFont("", 20, False)
font_s30_bold = pygame.font.SysFont("", 30, True)
font_s30 = pygame.font.SysFont("", 30, False)
seguisym_font_s30 = pygame.font.Font(FONT_SOURCE + "\\seguisym.ttf", 30)
font_s50_bold = pygame.font.SysFont("", 50, True)
font_s50 = pygame.font.SysFont("", 50, False)

START_POINT = (20, 720 - 60 * 10 - 20)

tower_slot = [Tower, Tower_AOE, Tower_Piercing, Tower_Farm, Tower, Tower]
tower_price = []
picking = None

for t in tower_slot:
    data = t(-1, -1)
    tower_price.append(data.price)


def draw_map(screen, map_game):
    # 14x10
    size_grip = 60
    x_point = 0
    y_point = 0
    pygame.draw.rect(screen, (100, 200, 100), (0, 0, 60 * 14, 60 * 10))
    for y in map_game:
        for x in y:
            if x != -2:
                pygame.draw.rect(
                    screen, (50, 50, 50), (x_point, y_point, size_grip, size_grip)
                )
            x_point += size_grip
        y_point += size_grip
        x_point = 0


def draw_house_health(screen, health, max_health):
    x = 20
    y = 20
    w = 14 * 30
    h = 30

    w_stat = w * (health / max_health)
    pygame.draw.rect(screen, (10, 10, 10), (x, y, w, h))
    pygame.draw.rect(screen, (30, 120, 30), (x, y, w_stat, h))
    pygame.draw.rect(screen, (120, 120, 120), (x, y, w, h), 5)
    text_label = font_s30_bold.render(f"{health}/{max_health}", False, (255, 255, 255))
    text_rect = text_label.get_rect()
    stat_rect = pygame.Rect(x, y, w, h)
    text_rect.center = stat_rect.center
    # pygame.draw.rect(screen,(255,0,0), text_rect)
    # text_rect.centery = stat_rect.centery
    screen.blit(text_label, (text_rect.x, text_rect.y))


def draw_money_stat(screen, money):
    x = 20
    y = 60
    w = 14 * 30
    h = 30

    # w_stat = w * (health / max_health)
    # pygame.draw.rect(screen, (10, 10, 10), (x, y, w, h))
    # pygame.draw.rect(screen, (30, 120, 30), (x, y, w_stat, h))
    # pygame.draw.rect(screen, (120, 120, 120), (x, y, w, h), 5)
    text_label = font_s30_bold.render(f"{money}💰", False, (255, 255, 255))
    text_rect = text_label.get_rect()
    stat_rect = pygame.Rect(x, y, w, h)
    text_rect.center = stat_rect.center
    # pygame.draw.rect(screen,(255,0,0), text_rect)
    # text_rect.centery = stat_rect.centery
    screen.blit(text_label, (text_rect.x, text_rect.y))


def draw_wave(screen, wave):
    text_label = font_s50.render(f"wave", False, (255, 255, 255))
    screen.blit(text_label, (G_SIZE_SCREEN[0] / 2 - text_label.get_width() / 2, 10))
    text_label2 = font_s50_bold.render(f"{wave}", False, (255, 255, 255))
    screen.blit(text_label2, (G_SIZE_SCREEN[0] / 2 - text_label2.get_width() / 2, 50))


def draw_fps(screen):
    fps = round(G_clock.get_fps())
    text_label = font_s50_bold.render(f"{fps}", False, (0, 0, 0))
    screen.blit(text_label, (G_SIZE_SCREEN[0] - 50, 10))


def draw_tower_stat(screen, tower):
    size_map = (60 * 14, 60 * 10)

    mx, my = pygame.mouse.get_pos()
    if tower.self_hitbox.collidepoint(mx - START_POINT[0], my - START_POINT[1]):

        y_pos = 0
        # emoji = ["🔼💀💦🔥🔦⏱❄⬆💥💤⏳⌛💸"]
        text = seguisym_font_s30.render(
            f"level - {tower.level} [↗]", True, (255, 255, 255)
        )
        r = text.get_rect()
        r.center = (
            START_POINT[0] + size_map[0] + 200,
            START_POINT[1] + 20 + y_pos,
        )
        screen.blit(text, (r.x, r.y))

        y_pos += 30

        for k, v in tower.stat_show.items():
            text_ = seguisym_font_s30.render(f"{k}: {v}", True, (255, 255, 255))
            r_ = text_.get_rect()
            screen.blit(
                text_,
                (START_POINT[0] + size_map[0] + 30, START_POINT[1] + 20 + y_pos),
            )
            y_pos += 30
        text = (
            f"Cost upgrade: {tower.cost}$"
            if tower.cost != "MAXED"
            else f"cost upgrade: MAXED"
        )
        text_ = seguisym_font_s30.render(text, True, (255, 255, 255))
        r_ = text_.get_rect()
        screen.blit(
            text_,
            (
                START_POINT[0] + size_map[0] + 30,
                START_POINT[1] + size_map[1] / 2 - r_.h - 15,
            ),
        )


def draw_pick_gui(screen):
    size_map = (60 * 14, 60 * 10)
    pygame.draw.rect(
        screen,
        (120, 120, 120),
        (
            START_POINT[0] + size_map[0] + 15,
            START_POINT[1],
            350,
            size_map[1] / 2,
        ),
        border_radius=10,
    )

    start_point = (
        START_POINT[0] + size_map[0] + 15,
        START_POINT[1] + size_map[1] / 2 + 15,
    )
    pygame.draw.rect(
        screen,
        (120, 120, 120),
        (
            start_point[0],
            start_point[1],
            350,
            size_map[1] / 2 - 15,
        ),
        border_radius=10,
    )
    padding = 15

    inside_width = 350 - 2 * 15
    inside_height = size_map[1] / 2 - 15 - 2 * 15
    idx = 0
    for i in range(2):
        for j in range(3):
            x = start_point[0] + padding / 2 + j * (inside_width / 3 + padding / 2)
            y = start_point[1] + padding / 2 + i * (inside_height / 2 + padding / 2) + 5

            pygame.draw.rect(
                screen,
                (140, 140, 140),
                (
                    x,
                    y,
                    inside_width / 3,
                    inside_height / 2,
                ),
                border_radius=5,
            )
            pygame.draw.rect(
                screen,
                (150, 150, 150),
                (
                    x,
                    y + inside_height / 2 / 2 + 30,
                    inside_width / 3,
                    inside_height / 2 - inside_height / 2 / 2 - 30,
                ),
                border_radius=5,
            )
            tower_data = tower_price[idx]
            text = font_s30_bold.render(
                f"{tower_data}$",
                False,
                (0, 0, 0),
            )
            r_ = text.get_rect()
            # r1 = (x + inside_width / 3, y + inside_height / 2)
            r1 = pygame.Rect(
                x,
                y + inside_height / 2 / 2 + 30,
                inside_width / 3,
                inside_height / 2 - inside_height / 2 / 2 - 30,
            )
            r_.center = r1.center

            # screen.blit(text, (r1[0] - r_.w - 15, r1[1] - r_.h - 5))
            screen.blit(text, (r_.x, r_.y))

            if picking == idx:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (
                        x,
                        y,
                        inside_width / 3,
                        inside_height / 2,
                    ),
                    width=5,
                    border_radius=5,
                )
            idx += 1


def render(
    p1,
    p2,
    map_game,
    enemys,
    towers,
    health,
    max_health,
    wave,
    money,
    screen: pygame.Surface,
):
    screen.fill((100, 100, 100))
    draw_house_health(screen, health, max_health)
    draw_money_stat(screen, money)
    size_map = (60 * 14, 60 * 10)
    map_surface = pygame.Surface(size_map)
    draw_map(map_surface, map_game)
    draw_pick_gui(screen)
    for enemy in enemys:
        enemy.render(map_surface)
    for tower in towers:
        tower.render(map_surface)
        draw_tower_stat(screen, tower)

    screen.blit(map_surface, START_POINT)
    draw_fps(screen)
    draw_wave(screen, wave)
    p1.render(screen)
    p2.render(screen)

    pygame.display.update()


def place_and_upgrade():
    global picking
    place_state = True
    upgrade_towers_idx = -1

    for twr in towers:
        upgrade_towers_idx += 1
        if twr.check_collide(p1):
            place_state = False
            break

    if place_state == True:
        if picking == None:
            return
        center = p1.get_center()
        test_tower = Tower(center[0], center[1])
        can_place = True

        for twr in towers:
            if twr.check_collide(test_tower):
                can_place = False
                break
        if can_place == True:
            new_tower = tower_slot[picking](
                center[0] - START_POINT[0], center[1] - START_POINT[1]
            )
            p1.towers.append(new_tower)
            picking = None
    else:
        p1.upgrade_towers.append(upgrade_towers_idx)


if __name__ == "__main__":
    network = Network()
    data = network.get_data()
    p1 = data[0]
    p2 = Player(100, 100, (50, 50, 255))
    map_game = data[1]
    enemys = []
    towers = []
    max_house_health = data[2]
    house_health = data[2]
    p1.health = max_house_health
    wave = 0
    money = 0

    while L_run:
        G_clock.tick(G_FPS)
        fps = G_clock.get_fps()
        t = G_FPS / (fps + 0.00001)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                L_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    place_and_upgrade()
                elif event.key == pygame.K_1:
                    picking = 0
                elif event.key == pygame.K_2:
                    picking = 1
                elif event.key == pygame.K_3:
                    picking = 2
                elif event.key == pygame.K_4:
                    picking = 3

        data = network.send(p1)
        if data:
            p2 = data[0]
            enemys = data[1]
            house_health = p2.health
            towers = data[2]
            p1.towers = []
            p1.upgrade_towers = []
            wave = data[3]
            money = data[4]
        # else:
        #     print(1222)

        p1.move(t)
        render(
            p1,
            p2,
            map_game,
            enemys,
            towers,
            house_health,
            max_house_health,
            wave,
            money,
            G_screen,
        )

    pygame.quit()
    os._exit(0)
