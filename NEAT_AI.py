import pygame as pg
import math as mt
import numpy as np
import neat
import os
from car import Car

pg.font.init()
font = pg.font.SysFont('georgia', 30)
window = pg.display.set_mode((1200, 900))
pg.display.set_caption("Self Driving Cars")
track_imgs = [pg.image.load("assets/track3.png"), pg.image.load("assets/track1.png"), pg.image.load("assets/track3.png"),
              pg.image.load("assets/track2.png"), pg.image.load("assets/track3.png"), pg.image.load("assets/track4.png")]
outline_imgs = [pg.image.load("assets/track3 outline.png"), pg.image.load("assets/track1 outline.png"), pg.image.load("assets/track3 outline.png"),
                pg.image.load("assets/track2 outline.png"), pg.image.load("assets/track3 outline.png"), pg.image.load("assets/track4 outline.png")]
fin_lines = [pg.image.load("assets/track3 fl.png"), pg.image.load("assets/track1 fl.png"), pg.image.load("assets/track3 fl.png"),
             pg.image.load("assets/track2 fl.png"), pg.image.load("assets/track3 fl.png"), pg.image.load("assets/track4 fl.png")]
gens = -1
track_num = 0
ln_line = 100
line = pg.transform.scale(pg.image.load("assets/line.png"), (ln_line, 1))
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)


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

    # window.blit(line1, off1)
    # window.blit(line2, off2)
    # window.blit(line3, off3)
    # window.blit(line4, off4)
    # window.blit(line5, off5)
    # window.blit(line6, off6)
    # window.blit(line7, off7)
    # window.blit(line8, off8)
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]

    offset = [off1, off2, off3, off4, off5, off6, off7, off8]
    points = []
    for i in range(len(lines)):
        mask = pg.mask.from_surface(lines[i])
        point = boundary.overlap(mask, offset[i])

        if point:
            # pg.draw.circle(window, red, point, 3)
            points.append(point)
        else:
            points.append((np.inf, np.inf))
    return points


def main(genomes, config):
    cars = []
    nets = []
    ge = []
    global gens
    global track_num
    img_num = track_num
    gens += 1
    track_img = track_imgs[img_num]
    outline_img = outline_imgs[img_num]
    fin_line = fin_lines[img_num]
    pos = [(275, 90), (550, 50), (275, 90), (800, 60), (275, 90), (350, 40)]
    xp, yp = pos[img_num]

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(xp, yp, 5))
        g.fitness = 0
        ge.append(g)

    track_outline = pg.mask.from_surface(outline_img)
    fin_mask = pg.mask.from_surface(fin_line)

    d = [0]*8
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()

        keys = pg.key.get_pressed()
        l = len(cars)
        text1 = font.render(f'Cars left: {l}', True, white)
        text2 = font.render(f'Generation: {gens}', True, white)
        if l == 0:
            break
        if keys[pg.K_RETURN]:
            track_num += 1
            pg.time.delay(100)
            break

        window.fill(black)
        window.blit(track_img, (0, 0))
        window.blit(fin_line, (0, 0))
        window.blit(outline_img, (0, 0))
        window.blit(text1, (20, 20))
        window.blit(text2, (20, 55))

        for x, c in enumerate(cars):
            c.move()
            if c.collide(track_outline):
                cars.pop(x)
                ge[x].fitness -= 0.1
                ge.pop(x)
                nets.pop(x)
                continue

            if c.collide(fin_mask):
                cars.pop(x)
                ge[x].fitness += 0.1
                ge.pop(x)
                nets.pop(x)
                continue

            ge[x].fitness += 0.01
            ofs = draw_lines(c.angle, c.x, c.y, c.car_img.get_width(), c.car_img.get_height(), track_outline)
            for k, p in enumerate(ofs):
                d[k] = (p[0] - c.offset[0] - c.rotated_image.get_width() // 2) ** 2 + (
                            p[1] - c.offset[1] - c.rotated_image.get_height() // 2) ** 2
            output = nets[x].activate((d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
            if min(np.round(output) == np.ones([2])):
                c.rotate(True)
            elif min(np.round(output) == np.zeros([2])):
                c.rotate(False)

        d_count = 0
        for c in cars:
            d_count += 1
            if d_count > 25:
                c.draw(window, False)
            else:
                c.draw(window)
        pg.display.update()


# ----------------------------------------------------NEAT--------------------------------------------------------

def run(c_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, c_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 200)
    print(f"\nBest genome:\n {winner}")


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    conf_path = os.path.join(local_dir, "config-ffnn.txt")
    run(conf_path)
