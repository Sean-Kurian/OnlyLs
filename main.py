import flet
from Window import Window

def main(page: flet.Page):
    page.title = 'LoL Lobby Lookup'
    page.window_height = 800
    page.window_width = 400
    page.window_resizable = False
    page.window_minimizable = True
    page.window_maximizable = False

    # TODO: Error checking if league client isn't open

    # Main Window Elements
    window = Window()
    page.add(window)


flet.app(target=main, assets_dir='images')
