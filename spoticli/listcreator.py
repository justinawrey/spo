import re
import sys

class PrettyListCreator:
    def __init__(self, input_data): # input_data = 2D array of data
        self.num_rows = len(input_data) + 1
        self.num_cols = len(input_data[0])
        if self.num_cols == 1:
            input_data.insert(0, ['Artist'])
        elif self.num_cols == 2:
            input_data.insert(0, ['Album', 'Artist'])
        elif self.num_cols == 3:
            input_data.insert(0, ['Song', 'Artist', 'Album'])
        self.col_width = max(len(word) for row in input_data for word in row) + 4
        input_data.insert(1, ['=' * self.col_width for x in range(self.num_cols)])
        self.input_data = input_data
        self.text = ''

    def pretty_list(self, highlight_row=0):
        index = 0
        rtn_str = ''
        for row in self.input_data:
            print_str = ''
            for word in row:
                print_str += "".join(word.ljust(self.col_width))
            if index == highlight_row + 2: # skip first row
                print_str = '\x1b[6;30;42m' + print_str + '\x1b[0m'
            rtn_str += print_str + '\n'
            index += 1
        return '\n' + rtn_str

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
