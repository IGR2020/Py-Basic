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
pg.display.set_caption(name)
while run:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    window.blit(assets['smile.jpeg'], (100, 100))
    pg.display.update()
    window.fill(background)
    text_colour = (90, 10, 30)
    EPT.blit_text(window, name, pos=(400, 200), colour=text_colour)
    EPT.blit_text(window, 'is this good', pos=(400, 250), colour=text_colour)
pg.quit()
quit()
