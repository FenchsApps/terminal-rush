
import curses
import time
import random
import argparse

def main(stdscr, difficulty):
    # Initial setup
    curses.curs_set(0) # Hide cursor during start screen
    stdscr.nodelay(0) # Wait for input on start screen

    # Set color scheme
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # --- Start Screen ---
    start_game = False
    while not start_game:
        stdscr.clear()

        # Title
        title = "Terminal-Rush: Kernel Panic"
        stdscr.addstr(height // 2 - 4, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)

        # Difficulty
        difficulty_text = f"Difficulty: {difficulty}"
        stdscr.addstr(height // 2, (width - len(difficulty_text)) // 2, difficulty_text, curses.color_pair(1))

        # Start message
        start_message = "Press Enter to start"
        stdscr.addstr(height // 2 + 2, (width - len(start_message)) // 2, start_message, curses.color_pair(1))

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_ENTER or key == 10:
            start_game = True
    # --- End of Start Screen ---


    # Setup for the game itself
    curses.curs_set(1) # Show cursor for command line
    stdscr.nodelay(1) # Don't block for input in game loop

    # Difficulty settings
    difficulty_settings = {
        "super-easy": {"spawn_rate": 0.02, "speed": 200},
        "easy": {"spawn_rate": 0.05, "speed": 150},
        "med": {"spawn_rate": 0.1, "speed": 100},
        "hard": {"spawn_rate": 0.2, "speed": 75},
        "very-hard": {"spawn_rate": 0.3, "speed": 50}
    }
    
    current_difficulty = difficulty_settings[difficulty]
    stdscr.timeout(current_difficulty['speed'])


    # Game state
    score = 0
    cpu_charge = 100
    processes = []
    game_over = False
    command = ""

    # Process data
    process_names = ["ls", "cp", "rm", "cat", "grep", "awk", "sed", "bash"]

    # Game loop
    while not game_over:
        # Handle input
        key = stdscr.getch()
        if key != -1:
            if key == curses.KEY_ENTER or key == 10:
                if command.startswith("kill -9 "):
                    try:
                        pid_to_kill = int(command.split(" ")[2])
                        found_process = False
                        for p in processes:
                            if p['pid'] == pid_to_kill:
                                processes.remove(p)
                                score += 10
                                found_process = True
                                break
                        if not found_process:
                            cpu_charge -= 5 # Penalty for wrong PID
                    except (ValueError, IndexError):
                        pass # Ignore invalid commands
                command = ""
            elif key == curses.KEY_BACKSPACE or key == 127:
                command = command[:-1]
            elif 32 <= key <= 126:
                command += chr(key)


        # Game logic
        # - Generate new processes
        if random.random() < current_difficulty['spawn_rate']:
            process_name = random.choice(process_names)
            pid = random.randint(1000, 9999)
            x = random.randint(1, width - 25)
            processes.append({'pid': pid, 'name': process_name, 'x': x, 'y': 2})

        # - Move processes down
        for p in processes:
            p['y'] += 1
            if p['y'] > height - 3:
                processes.remove(p)
                cpu_charge -= 10


        # Drawing
        stdscr.clear()

        # Draw borders
        log_height = height // 3
        stdscr.addstr(0, 0, "SYSTEM LOG".center(width, "="), curses.color_pair(1))
        for i in range(1, log_height):
             stdscr.addstr(i, 0, "|", curses.color_pair(1))
             stdscr.addstr(i, width-1, "|", curses.color_pair(1))
        stdscr.addstr(log_height, 0, "=" * width, curses.color_pair(1))

        target_area_height = height - log_height - 2
        
        stdscr.addstr(height - 2, 0, "=" * width, curses.color_pair(1))


        # Draw score and cpu
        stdscr.addstr(0, 1, f"Score: {score} | CPU Charge: {cpu_charge}%", curses.color_pair(1))

        # Draw falling processes
        for p in processes:
           stdscr.addstr(p['y'], p['x'], f"[PID {p['pid']}] {p['name']}", curses.color_pair(1))

        # Draw command line
        stdscr.addstr(height - 1, 0, f"root@localhost:~# {command}", curses.color_pair(1))


        stdscr.refresh()

        # Check for game over
        if cpu_charge <= 0:
            cpu_charge = 0
            game_over = True
            
    # Game over screen
    stdscr.nodelay(0) # Wait for user input
    stdscr.clear()
    game_over_msg = "KERNEL PANIC!"
    final_score_msg = f"Final Score: {score}"
    stdscr.addstr(height // 2 -1, (width - len(game_over_msg)) // 2, game_over_msg, curses.color_pair(1))
    stdscr.addstr(height // 2, (width - len(final_score_msg)) // 2, final_score_msg, curses.color_pair(1))
    stdscr.addstr(height // 2 + 2, (width - len("Press any key to exit")) // 2, "Press any key to exit", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Terminal Rush: Kernel Panic')
    parser.add_argument('--dif', type=str, choices=['super-easy', 'easy', 'med', 'hard', 'very-hard'], default='med', help='Set the game difficulty')
    args = parser.parse_args()

    try:
        curses.wrapper(main, difficulty=args.dif)
    except curses.error as e:
        print(f"There was an error with curses: {e}")
        print("Your terminal may not be compatible. Try running in a different terminal.")

