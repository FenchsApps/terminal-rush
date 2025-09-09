# Terminal Rush: Kernel Panic

**Slogan:** Your terminal is the battlefield. Don't let rogue processes cause a Kernel Panic!

## Game Concept

You are a system administrator (root user). A malicious virus (0xDEADBEEF) has attacked your system, corrupting executable files and turning system utilities (ls, cp, rm, cat, etc.) into hostile processes. Your mission is to find and "kill" these processes before they overload the system and trigger a Kernel Panic.

This game is a hybrid of an arcade and a terminal simulator with reaction-testing elements.

## Gameplay

The game is played in a terminal window, with the interface split into three parts:

*   **Top 1/3: System Event Log:** A real-time log of system events, simulating the output of `dmesg -w` and `journalctl -f`. Among normal messages, warnings about corrupted binaries and unusual resource consumption will appear.
*   **Middle 1/3: Target Area:** This is where the targets appear—lines containing the PID (Process ID) and the name of the corrupted executable. They "fall" from top to bottom, like in classic arcade games.
*   **Bottom Line: Command Line:** As the root user, you must quickly type the `kill -9 <PID>` command here to "shoot down" the falling process before it disappears off the bottom of the screen.

### Mechanics

*   Processes fall with increasing speed depending on the chosen difficulty.
*   Enter the correct `kill -9 <PID>` and press Enter to destroy a process and increase your score.
*   If you make a mistake with the PID, or if a process reaches the bottom of the screen, your CPU Charge (health) decreases.
*   The game ends when your CPU Charge drops to 0%, displaying the classic Kernel Panic message.

## How to Run

1.  Make sure you have Python 3 installed.
2.  Run the game from your terminal:

    ```bash
    python main.py
    ```

### Difficulty Levels

You can set the game's difficulty using the `--dif` flag.

*   `--dif super-easy`
*   `--dif easy`
*   `--dif med` (default)
*   `--dif hard`
*   `--dif very-hard`

**Example:**

```bash
python main.py --dif hard
```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) file for details.
