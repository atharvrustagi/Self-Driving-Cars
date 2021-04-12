import pygame as pg
import math as mt
import numpy as np
from car import Car

window = pg.display.set_mode((1200, 900))
track_img = pg.image.load("track2.png")
outline_img = pg.image.load("track2 outline.png")
ln_line = 100
line = pg.transform.scale(pg.image.load("line.png"), (ln_line, 1))
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)


def draw_lines(ang, x, y, w, ln, boundary):
    cos = round(ln_line * mt.cos(mt.radians(ang)))
    sin = round(ln_line * mt.sin(mt.radians(ang)))
    line1 = pg.transform.rotate(line, ang)
    line2 = pg.transform.rotate(line, ang)
    line3 = pg.transform.rotate(line, (ang + 90) % 360)
    line4 = pg.transform.rotate(line, (ang + 90) % 360)
    if ang in range(270, 360):
        off1 = (x + w // 2, y + ln // 2)
        off2 = (x + w // 2 - cos, y + ln // 2 + sin)
        off3 = (x + w // 2, y + ln // 2 - cos)
        off4 = (x + w // 2 + sin, y + ln // 2)
    elif ang in range(90):
        off1 = (x + w // 2, y + ln // 2 - sin)
        off2 = (x + w // 2 - cos, y + ln // 2)
        off3 = (x + w // 2 - sin, y + ln // 2 - cos)
        off4 = (x + w // 2, y + ln // 2)
    elif ang in range(90, 180):
        off1 = (x + w // 2 + cos, y + ln // 2 - sin)
        off2 = (x + w // 2, y + ln // 2)
        off3 = (x + w // 2 - sin, y + ln // 2)
        off4 = (x + w // 2, y + ln // 2 + cos)
    else:
        off1 = (x + w // 2 + cos, y + ln // 2)
        off2 = (x + w // 2, y + ln // 2 + sin)
        off3 = (x + w // 2, y + ln // 2)
        off4 = (x + w // 2 + sin, y + ln // 2 + cos)
    
    line5 = pg.transform.rotate(line, (ang + 45) % 360)
    line6 = pg.transform.rotate(line, (ang + 45) % 360)
    line7 = pg.transform.rotate(line, (ang - 45) % 360)
    line8 = pg.transform.rotate(line, (ang - 45) % 360)
    ang = (ang - 45) % 360
    cos = round(ln_line * mt.cos(mt.radians(ang)))
    sin = round(ln_line * mt.sin(mt.radians(ang)))
    # off7, off8, off6, off5 respectively behave like off1, off2, off3, off4 in the same range
    if ang in range(270, 360):
        off7 = (x + w // 2, y + ln // 2)
        off8 = (x + w // 2 - cos, y + ln // 2 + sin)
        off6 = (x + w // 2, y + ln // 2 - cos)
        off5 = (x + w // 2 + sin, y + ln // 2)
    elif ang in range(90):
        off7 = (x + w // 2, y + ln // 2 - sin)
        off8 = (x + w // 2 - cos, y + ln // 2)
        off6 = (x + w // 2 - sin, y + ln // 2 - cos)
        off5 = (x + w // 2, y + ln // 2)
    elif ang in range(90, 180):
        off7 = (x + w // 2 + cos, y + ln // 2 - sin)
        off8 = (x + w // 2, y + ln // 2)
        off6 = (x + w // 2 - sin, y + ln // 2)
        off5 = (x + w // 2, y + ln // 2 + cos)
    else:
        off7 = (x + w // 2 + cos, y + ln // 2)
        off8 = (x + w // 2, y + ln // 2 + sin)
        off6 = (x + w // 2, y + ln // 2)
        off5 = (x + w // 2 + sin, y + ln // 2 + cos)

    window.blit(line1, off1)
    window.blit(line2, off2)
    window.blit(line3, off3)
    window.blit(line4, off4)
    window.blit(line5, off5)
    window.blit(line6, off6)
    window.blit(line7, off7)
    window.blit(line8, off8)

    lines = [line1, line2, line3, line4, line5, line6, line7, line8]
    offset = [off1, off2, off3, off4, off5, off6, off7, off8]
    points = []
    for i in range(len(lines)):
        mask = pg.mask.from_surface(lines[i])
        point = boundary.overlap(mask, offset[i])

        if point:
            pg.draw.circle(window, red, point, 3)
            points.append(point)
        else:
            points.append((np.inf, np.inf))
    return points


def draw(c, outline):
    window.fill((0,0,0))
    window.blit(track_img, (0, 0))
    window.blit(outline_img, (0, 0))
    off = draw_lines(c.angle, c.x, c.y, c.car_img.get_width(), c.car_img.get_height(), outline)
    c.draw(window)
    pg.display.update()
    return off


def main():
    car = Car(300, 90, 3)
    track_outline = pg.mask.from_surface(outline_img)
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            car.rotate(False)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            car.rotate(True)

        pp = draw(car, track_outline)
        d = [0]*8
        for x, p in enumerate(pp):
            d[x] = (p[0]-car.offset[0]-car.rotated_image.get_width()//2)**2 + (p[1]-car.offset[1]-car.rotated_image.get_height()//2)**2
        print(d)
        car.move()
        car.collide(track_outline)


main()
