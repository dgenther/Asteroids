



'''FONT STUFF'''
title_font_size = 100
font_string = '../assets/joystix monospace.ttf'
title_letter_pixel_size = title_font_size / 1.2 #roughly        
title_string = 'ASTEROIDS'
title_line_length = len(title_string)
title_x_offset = title_letter_pixel_size * len(title_string) / 2
title_y_offset = 0
menu_font_size = 40
menu_letter_pixel_size = menu_font_size / 1.2 #roughly
StartString = 'START'
OptionsString = 'OPTIONS'
QuitString = 'QUIT'
menu_x_offset_start = menu_letter_pixel_size * len(StartString) / 2
menu_x_offset_options = menu_letter_pixel_size * len(OptionsString) / 2
menu_x_offset_quit = menu_letter_pixel_size * len(QuitString) / 2

colors = {
    'black': (0,0,0),           # used for background
    'white': (255,255,255),     #
    'green': (0,150,0),
    'red': (150,0,0),
    'blue': (0,0,150),
}
states = {  'menu': True, 
            'game': False, 
            'options': False, 
            'pause': False
}

def fill_window_color(game, color: str):
    game.game_window.fill(colors.get(color))