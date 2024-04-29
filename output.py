import pygame as pg
import EPT

assets={}

window_width, window_height = 900, 500
window=pg.display.set_mode((window_width, window_height))
background = (255, 255, 255)

clock = pg.time.Clock()
fps=60
run = True

assets.update(EPT.load_assets('assets'))
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    window.blit(assets['smile.jpeg'], (100, 100))
    pg.display.update()
    window.fill(background)
pg.quit
quit()
