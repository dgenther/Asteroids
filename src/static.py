



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
start_string = 'START'
options_string = 'OPTIONS'
quit_string = 'QUIT'
retry_string = 'RETRY'
dead_string = 'YOU DIED'
dead_line_length = len(dead_string)
menu_x_offset_start = menu_letter_pixel_size * len(start_string) / 2
menu_x_offset_options = menu_letter_pixel_size * len(options_string) / 2
menu_x_offset_quit = menu_letter_pixel_size * len(quit_string) / 2
dead_x_offset_dead = title_letter_pixel_size * len(dead_string) / 2
dead_x_offset_retry = menu_letter_pixel_size * len(retry_string) / 2
dead_x_offset_quit = menu_letter_pixel_size * len(quit_string) / 2

'''COLORS'''
colors = {
    'black': (0,0,0),           # used for background
    'white': (255,255,255),     #
    'green': (0,150,0),
    'red': (150,0,0),
    'blue': (0,0,150),
    'red': (238,75,43)
}

'''STATES'''
states = {  'menu': True, 
            'game': False, 
            'options': False, 
            'pause': False,
            'dead': False,
}

def fill_window_color(game, color: str):
    game.game_window.fill(colors.get(color))