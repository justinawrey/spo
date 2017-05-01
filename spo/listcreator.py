import re
import sys

class PrettyListCreator:
    def __init__(self, input_data): # input_data = 2D array of data
        num_cols = len(input_data[0])
        self.col_widths = []
        for col in range(num_cols):
            self.col_widths.append(max(len(row[col]) for row in input_data) + 4)

        # header stuff
        if num_cols == 1:
            input_data.insert(0, ['Artist'])
        elif num_cols == 2:
            input_data.insert(0, ['Album', 'Artist'])
        elif num_cols == 3:
            input_data.insert(0, ['Song', 'Artist', 'Album'])
        input_data.insert(1, ['=' * width for width in self.col_widths])

        self.input_data = input_data
        self.text = ''

    def pretty_list(self, highlight_row=0):
        index = 0
        rtn_str = ''
        for row in self.input_data:
            print_str = ''
            for col in range(len(self.col_widths)):
                print_str += row[col].ljust(self.col_widths[col])
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
