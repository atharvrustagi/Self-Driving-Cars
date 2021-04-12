import math as mt
import pygame as pg


class Car:

    car_img = pg.image.load("assets/car1.png")
    car_img = pg.transform.scale(car_img, (50, 50))

    def __init__(self, x, y, vel, angle=270):
        self.x = x
        self.y = y
        self.vel = vel
        self.angle = angle
        self.rotated_image = pg.transform.rotate(self.car_img, self.angle)
        self.offset = (0, 0)
        self.count = 0

    def rotate(self, clockwise):
        if not clockwise:
            self.angle += self.vel + 1
        else:
            self.angle -= self.vel + 1
        self.angle = self.angle % 360

    def move(self):
        ang = mt.radians(self.angle)
        self.x -= round(self.vel * mt.sin(ang))
        self.y -= round(self.vel * mt.cos(ang))

    def draw(self, win, blit=True):
        self.rotated_image = pg.transform.rotate(self.car_img, self.angle)
        new_rect = self.rotated_image.get_rect(center=self.car_img.get_rect(topleft=(self.x, self.y)).center)
        if blit:
            win.blit(self.rotated_image, new_rect)
        self.offset = (new_rect[0], new_rect[1])

    def mask(self):
        return pg.mask.from_surface(self.rotated_image)

    def collide(self, track_outline):
        ov = track_outline.overlap(self.mask(), self.offset)
        if ov:
            # self.count += 1
            # print("boom "+str(self.count))
            return True
        return False
