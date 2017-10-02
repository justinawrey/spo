def print_table(input_data):
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
    for row in input_data:
        _ = [print(("| " + row[i]).ljust(col_widths[i] + 3), end='') for i in range(3)]
        print('|')

    # print footer
    _ = [print('=' * (col + 3), end='') for col in col_widths]
    print('=')
