import curses
import random


def main(stdscr):
    # Curses settings
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    # Screen dimensions
    sh, sw = stdscr.getmaxyx()
    if sh < 20 or sw < 40:
        stdscr.nodelay(False)
        stdscr.addstr(0, 0, "Terminal window is too small. Press any key to exit.")
        stdscr.getch()
        return

    # Initial snake setup (center of screen)
    snk_y = sh // 2
    snk_x = sw // 4
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2],
    ]

    # Initial food placement
    food = [sh // 2, sw // 2]
    stdscr.addch(food[0], food[1], "*")

    key = curses.KEY_RIGHT
    score = 0

    key_map = {
        ord('w'): curses.KEY_UP,
        ord('W'): curses.KEY_UP,
        ord('s'): curses.KEY_DOWN,
        ord('S'): curses.KEY_DOWN,
        ord('a'): curses.KEY_LEFT,
        ord('A'): curses.KEY_LEFT,
        ord('d'): curses.KEY_RIGHT,
        ord('D'): curses.KEY_RIGHT,
        curses.KEY_UP: curses.KEY_UP,
        curses.KEY_DOWN: curses.KEY_DOWN,
        curses.KEY_LEFT: curses.KEY_LEFT,
        curses.KEY_RIGHT: curses.KEY_RIGHT,
    }

    opposites = {
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP,
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_RIGHT: curses.KEY_LEFT,
    }

    while True:
        next_key = stdscr.getch()
        if next_key != -1:
            if next_key in (27, ord('q'), ord('Q')):  # ESC veya Q ile cikis
                break
            mapped_key = key_map.get(next_key)
            if mapped_key and opposites[mapped_key] != key:
                key = mapped_key

        # Calculate new head position
        head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        # Check wall collision or self-collision
        if (
            head[0] in [0, sh - 1]
            or head[1] in [0, sw - 1]
            or head in snake
        ):
            msg = f"Oyun Bitti! Skor: {score} - Cikmak icin bir tusa basin"
            stdscr.addstr(sh // 2, max(0, (sw - len(msg)) // 2), msg)
            stdscr.nodelay(False)
            stdscr.getch()
            break

        snake.insert(0, head)

        # Check if food eaten
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                new_food = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2),
                ]
                if new_food not in snake:
                    food = new_food
            stdscr.addch(food[0], food[1], "*")
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], " ")

        # Draw borders, snake head and score
        stdscr.border(0)
        stdscr.addch(snake[0][0], snake[0][1], "#")
        stdscr.addstr(0, 2, f" Skor: {score} | Yon Tuşlari / WASD | Cikis: Q / ESC ")
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
