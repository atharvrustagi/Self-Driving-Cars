import pygame as pg
import math as mt


window = pg.display.set_mode((700, 700))
run = True


def draw_lines(ang):
    line1 = pg.transform.rotate(line, ang)
    line2 = pg.transform.rotate(line, ang)
    line3 = pg.transform.rotate(line, (ang + 90) % 360)
    line4 = pg.transform.rotate(line, (ang + 90) % 360)
    cos = round(ln_line*mt.cos(mt.radians(ang)))
    sin = round(ln_line*mt.sin(mt.radians(ang)))
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
    # off5 now behaves like off4 in the same range
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
    offsets = [off1, off2, off3, off4, off5, off6, off7, off8]
    for l in range(len(lines)):
        mask = pg.mask.from_surface(lines[l])
        point = out_mask.overlap(mask, (offsets[l][0]-blit_pt[0], offsets[l][1]-blit_pt[1]))
        if point:
            pg.draw.circle(window, (255,0,0), (point[0]+blit_pt[0], point[1]+blit_pt[1]), 10)
            # print(point)


def draw(ang):
    black = (0,0,0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    red = (255, 0, 0)
    window.fill(gray)
    window.blit(out_rect, blit_pt)
    rotated_box = pg.transform.rotate(box, ang)
    new_rect = rotated_box.get_rect(center=box.get_rect(topleft=(x, y)).center)
    window.blit(rotated_box, new_rect)
    draw_lines(ang)
    pg.display.update()


clock = pg.time.Clock()
out_rect = pg.image.load("assets/rect.png")
blit_pt = (0, 0)
box = pg.transform.scale(pg.image.load("assets/box.png"), (50, 50))
ln_line = 300
line = pg.transform.scale(pg.image.load("assets/line.png"), (ln_line, 2))
out_mask = pg.mask.from_surface(out_rect)
x = 300
y = 300
ln = box.get_height()
w = box.get_width()
angle = 0

while run:
    #clock.tick(90)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        x -= 2
    if keys[pg.K_d]:
        x += 2
    if keys[pg.K_w]:
        y -= 2
    if keys[pg.K_s]:
        y += 2
    if keys[pg.K_e]:
        angle -= 1
    if keys[pg.K_q]:
        angle += 1
    angle %= 360

    draw(angle)
pg.quit()
