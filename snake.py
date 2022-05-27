import curses
from curses import wrapper
import random
import time

snake_block = "\u2588"
foods = ["@", "$", "€", "£"]
wall = "SNAKE RUNS INTO WALL."
hit = "SNAKE RUNS INTO ITSELF."
g_o = "GAME OVER!"
t = "TIME: "
sc = "SCORE: "
fe = "FOODS EATEN: "
sl = "SNAKE LENGTH: "
game_speed = 100 
# to change the size of the map -> change the size of the terminal window
# if code gives error -> resize terminal window

def generate_random(bottom_constraint, top_constraint, snake):
    location = [0,0]
    while True:
        location[0] = random.randint(bottom_constraint, top_constraint)
        location[1] = random.randint(bottom_constraint, top_constraint)
        if location not in snake:
            break
    return location

def format_time(minutes, seconds):
    min = str(minutes).rjust(2, "0")
    sec = str(seconds).rjust(2, "0")
    formatted = "{}:{}".format(min, sec)
    return formatted

def timePassed(minutes, seconds, t):
    return t + format_time(minutes, seconds)

def main(stdscr):
    
    max_size = stdscr.getmaxyx()
    edge = max_size[0] if max_size[0] < max_size[1] else max_size[1]
    game_screen = curses.newwin(edge, edge, 0, 0)
    game_screen.border()
    game_screen.nodelay(1)
    game_screen.timeout(game_speed)
    game_screen.keypad(1)
    curses.curs_set(0)
    score = 0
    eaten_food_count = 0
    minutes = 0
    seconds = 0
    
    x = 3
    y = 1
    
    snake = [
        [y, x],
        [y, x-1],
        [y, x-2]
        ]

    offset = edge + 1 + len(sl)
    stdscr.addstr(0, edge + 1, sl, curses.A_BOLD)
    stdscr.addstr(1, offset - len(fe), fe, curses.A_BOLD)
    stdscr.addstr(2, offset - len(t), t, curses.A_BOLD)
    stdscr.addstr(3, offset - len(sc), sc, curses.A_BOLD)
    
    stdscr.addstr(0, offset, str(3 + eaten_food_count), curses.A_BOLD)
    stdscr.addstr(1, offset, str(eaten_food_count), curses.A_BOLD)
    stdscr.addstr(2, offset, format_time(minutes, seconds))
    stdscr.addstr(3, offset, str(score), curses.A_BOLD)
    
    for _ in range(len(snake)):
        game_screen.addstr(snake[_][0], snake[_][1], snake_block)

    rndm = generate_random(1, edge - 2, snake)
    game_screen.addstr(rndm[0], rndm[1], foods[0])

    key = curses.KEY_RIGHT
    ESC = 27 # ascii code
    start = time.time()
    while key != ESC:
        stdscr.refresh()
        next_key = game_screen.getch()
        key = key if next_key == -1 else next_key
        
        if (key not in [curses.KEY_LEFT, curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, ESC]):
            key = key
        
        if key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_UP:
            y -= 1 
        elif key == curses.KEY_RIGHT:
            x += 1
        elif key == curses.KEY_LEFT:
            x -= 1
        else:
            break

        food_eaten = False
        target = game_screen.inch(y, x)
        if  target in [64, 36, 8364, 163]:
            food_eaten = True
            eaten_food_count += 1
            if target == 64:
                score += 3
            elif target == 36: 
                score += 5
            elif target == 8364:
                score += 10
            elif target == 163:
                score += 50
                
            snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1]])
            rndm = generate_random(1, edge - 2, snake)
            if eaten_food_count % 15 == 0:
                game_screen.addstr(rndm[0], rndm[1], foods[3])
            elif eaten_food_count % 5 == 0:
                game_screen.addstr(rndm[0], rndm[1], foods[2])
            elif eaten_food_count % 3 == 0:
                game_screen.addstr(rndm[0], rndm[1], foods[1])
            else:
                game_screen.addstr(rndm[0], rndm[1], foods[0])
            
            stdscr.addstr(0, offset, str(3 + eaten_food_count), curses.A_BOLD)
            stdscr.addstr(1, offset, str(eaten_food_count), curses.A_BOLD)    
            stdscr.addstr(3, offset, str(score), curses.A_BOLD)
            stdscr.refresh()
        
        def game_over(id):
            game_screen.clear()
            game_screen.border()
            game_screen.addstr(1, (edge - len(id)) // 2, id, curses.A_BOLD)
            game_screen.addstr(2, (edge - len(g_o)) // 2, g_o, curses.A_BOLD)
            game_screen.refresh()
            time.sleep(3)
        
        if target == 9608:
            game_over(hit)
            break
        
        def boundary_check():
            const_y_1 = (y == 0)
            const_y_2 = (y == edge - 1)
            const_x_1 = (x == 0)
            const_x_2 = (x == edge - 1)
            case = const_y_1 or const_y_2 or const_x_1 or const_x_2
            return case
        
        if boundary_check():
            game_over(wall)
            break
          
        try:    
            game_screen.addch(y, x, snake_block)
        except curses.error:
            game_over(wall)
            break
            
        if not food_eaten:
            game_screen.addch(snake[len(snake)-1][0], snake[len(snake)-1][1], ' ')

        for s in range(len(snake) - 1, 0, -1):
            snake[s][0] = snake[s-1][0]
            snake[s][1] = snake[s-1][1]
        snake[0][0] = y
        snake[0][1] = x

        # horrible elapsed time calculation
        end = time.time()
        time_passed = end - start
        if 1 - time_passed < 0.00001:
            seconds += 1
            start = end
        if seconds == 60:
            minutes += 1
            seconds = 0
            
        f_time = format_time(minutes, seconds)
        stdscr.addstr(2, offset, f_time)
        
        stdscr.refresh()
        game_screen.refresh()
        
wrapper(main)