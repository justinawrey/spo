import re
import sys
import os

class PrettyListCreator:
    def __init__(self, input_data): # input_data = 2D array of data
        self.col_widths = []
        self.total_width = 0
        self.overflow = False
        for col in range(3):
            self.col_widths.append(max(len(row[col]) for row in input_data) + 4)
            self.total_width += self.col_widths[col]
        _, t_columns = os.popen('stty size', 'r').read().split() # get width of terminal
        if self.total_width > int(t_columns):
            self.overflow = True

        # header stuff
        input_data.insert(0, ['Song', 'Artist', 'Album'])
        self.input_data = input_data
        self.text = ''

    def pretty_list(self, highlight_row=0):
        index = 0
        rtn_str = ''
        for row in self.input_data:
            print_str = ''
            for col in range(3):
                print_str += row[col].ljust(self.col_widths[col])
            if self.overflow:
                print_str = print_str[:self.total_width - 3] + '...'
            if index == highlight_row + 2: # skip first two rows
                print_str = '\x1b[6;30;42m' + print_str + '\x1b[0m'
            rtn_str += print_str + '\n'
            index += 1
        return '\n' + rtn_str + '\n\nmove down:\t<j>\nmove up:\t<k>\nplay selection:\t<enter>\nquit:\t\t<q> or <esc>\n\n'

    def moveup(self, lines):
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        # Clear previous text by overwriting non-spaces with spaces
        self.moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self.moveup(lines)
        sys.stdout.write(text)
        self.text = text

# end ListCreator
