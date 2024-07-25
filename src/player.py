import pygame


class Player:
    def __init__(self, x: int, y: int, color: tuple[int]) -> None:
        self.x = x
        self.y = y

        self.w = 70
        self.h = 70

        self.speed = 3

        self.color = color
        self.health = 500

        self.towers = []
        self.upgrade_towers = []

    def get_center(self):
        return self.x + self.w / 2, self.y + self.h / 2

    def get_rect_all(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def get_rect(self):
        r = pygame.Rect(self.x, self.y, 20, 20)
        r.center = self.get_center()
        return r

    def get_graphic(self):
        surface = pygame.Surface((self.w, self.h))
        surface.set_colorkey((0, 0, 0))
        self.draw_border(surface)
        self.draw_cross(surface)
        return surface

    def draw_border(self, surface):
        pygame.draw.rect(surface, self.color, (0, 0, self.w, self.h), 7)
        r1 = pygame.Rect(0, 0, self.w / 2, self.h)
        r1.centerx = self.w / 2
        r2 = pygame.Rect(0, 0, self.w, self.h / 2)
        r2.centery = self.h / 2
        pygame.draw.rect(surface, (0, 0, 0), r1)
        pygame.draw.rect(surface, (0, 0, 0), r2)

    def draw_cross(self, surface):
        r1 = pygame.Rect(0, 0, 20, 5)
        r1.center = (self.w / 2, self.h / 2)
        r2 = pygame.Rect(0, 0, 5, 20)
        r2.center = (self.w / 2, self.h / 2)
        pygame.draw.rect(surface, self.color, r1)
        pygame.draw.rect(surface, self.color, r2)

    def move(self, tick):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_w]:
            self.y -= self.speed * tick
        if key_pressed[pygame.K_s]:
            self.y += self.speed * tick
        if key_pressed[pygame.K_a]:
            self.x -= self.speed * tick
        if key_pressed[pygame.K_d]:
            self.x += self.speed * tick

    def render(self, screen: pygame.Surface):
        graphic = self.get_graphic()
        screen.blit(graphic, (self.x, self.y))
