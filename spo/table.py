import time
import sys

from .getch import _Getch

ANSI_COLOR_BLUE_ON_WHITE = "\x1b[0;37;44m"
ANSI_END_ENC = "\x1b[0m"
ANSI_CLEAR_GO_TO_ORIGIN = "\x1b[2J"
ANSI_MOVE_CURSOR_UP = "\x1b[1A"
ANSI_MOVE_CURSOR_DOWN = "\x1b[1B"
ANSI_ENTER = "\r"
ANSI_ESC = "\x1b"
ANSI_CLEAR_LINE = "\x1b[2K"


def print_table(input_data, highlight_row=None, reprint_mode=False):
    """
    Prints a table of items having the format -

    ================================================================
    | SONG       | ARTIST      | ALBUM                             |
    ================================================================
    | Wonderwall | Oasis       | (What's The Story?) Morning Glory |
    | I Miss You | Blink-182   | Blink-182                         |
    ================================================================

        :param input_data {[string][string]}: A 2D array containing
        the data to be pretty printed. Width of 2D array must be 3.
        The first row (SONG, ARTIST, ALBUM) is automatically pre-pended
        to the displayed table.
        :param highlight_row {int}: row number of 2d array to be highlighted,
                                    highlight=None -> no highlighting (0-indexed)
        "param reprint_mode {bool}: whether to turn on reprint mode or not.
                                    Reprint mode causes printing to always be started
                                    from the top-left corner of the terminal.

    """

    # get the width each column must be to fit each columns widest
    # respective element
    col_widths = [4, 6, 5]  # default widths of SONG ARTIST ALBUM
    for col in range(3):
        col_max = max(len(row[col]) for row in input_data)
        if col_max > col_widths[col]:
            col_widths[col] = col_max

    # print header (use list comprehension printing hack)
    _ = [print('=' * (col + 3), end='') for col in col_widths]
    print('=')
    print("| SONG".ljust(col_widths[0] + 3)
          + "| ARTIST".ljust(col_widths[1] + 3)
          + "| ALBUM".ljust(col_widths[2] + 3) + '|')
    _ = [print('=' * (col + 3), end='') for col in col_widths]
    print('=')

    # print table data row by row
    row_num = 0
    for row in input_data:
        if row_num == highlight_row:
            print(ANSI_COLOR_BLUE_ON_WHITE, end='')
            _ = [print(("| " + row[i]).ljust(col_widths[i] + 3), end='')
                 for i in range(3)]
            print('|' + ANSI_END_ENC)
        else:
            _ = [print(("| " + row[i]).ljust(col_widths[i] + 3), end='')
                 for i in range(3)]
            print('|')
        row_num += 1

    # print footer
    _ = [print('=' * (col + 3), end='') for col in col_widths]
    print('=')

    if reprint_mode:
        # number of song data rows printed + number of extra pretty printing rows +
        # number of rows printed for user controls
        last_print_size = len(input_data) + 4 + 6
        print_user_controls()
        user_input = poll_for_user_input()

        if user_input == ANSI_ESC:
            clear_and_move_cursor_up(last_print_size)

        elif user_input == ANSI_ENTER:
            clear_and_move_cursor_up(last_print_size)

        elif user_input == 'k' or  user_input == ANSI_MOVE_CURSOR_UP:
            clear_and_move_cursor_up(last_print_size)
            if highlight_row > 0:
                print_table(input_data, highlight_row - 1, True)
            else:
                print_table(input_data, highlight_row, True)

        elif user_input == 'j' or  user_input == ANSI_MOVE_CURSOR_DOWN:
            clear_and_move_cursor_up(last_print_size)
            if highlight_row < len(input_data) - 1:
                print_table(input_data, highlight_row + 1, True)
            else:
                print_table(input_data, highlight_row, True)

        else:
            clear_and_move_cursor_up(last_print_size)
            print_table(input_data, highlight_row, True)


def print_user_controls():
    print("")
    print(" scroll up   : <k> or \u2191")
    print(" scroll down : <j> or \u2193")
    print(" select      : <enter>")
    print(" quit        : <esc>")
    print("")


def clear_and_move_cursor_up(num):
    for _ in range(num):
        sys.stdout.write(ANSI_MOVE_CURSOR_UP)
        sys.stdout.write(ANSI_CLEAR_LINE)
    sys.stdout.flush()


def poll_for_user_input():
    getch = _Getch()
    return getch()
