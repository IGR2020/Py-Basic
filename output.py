import pygame as pg
import EPT

assets={}

window_width, window_height = 900, 500
window=pg.display.set_mode((window_width, window_height))
background = (255, 255, 255)

clock = pg.time.Clock()
fps=60
run = True

text_colour=(0, 0, 0)

assets.update(EPT.load_assets('assets'))
name = "Bob"
pg.display.set_caption('Py-Basic')
x, y = (100, 100)
m = 1
v = 1.02
a = 1.001
while run:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    window.blit(assets['smile.jpeg'], (x, y))
    pg.display.update()
    window.fill(background)
    if window_width < x:
        m = -1
    if 0 > x:
        m = 1
    m *= v
    v *= a
    x += m
    text_colour = (90, 10, 30)
pg.quit()
quit()
