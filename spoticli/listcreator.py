import re
import sys
import time

class PrettyListCreator:
    def __init__(self, input_data): # input_data = 2D array of data
        input_data.insert(0, ['song', 'artist', 'album'])
        self.num_rows = len(input_data) - 1
        self.col_width = max(len(word) for row in input_data for word in row) + 2
        self.input_data = input_data
        self.text = ''

    def pretty_list(self, highlight_row=0):
        index = 0
        rtn_str = ''
        for row in self.input_data:
            print_str = ''
            for word in row:
                print_str += "".join(word.ljust(self.col_width))
            if index == highlight_row + 1: # skip first row
                print_str = '\x1b[6;30;42m' + print_str + '\x1b[0m'
            rtn_str += print_str + '\n'
            index += 1
        return rtn_str

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
'''
test_data = [['a', 'b', 'c'],
            ['aaa', 'b', 'c'],
            ['a', 'bbbb', 'c']]

listCreator = PrettyListCreator(test_data)

listCreator.reprint(listCreator.pretty_list(0))
time.sleep(1)
listCreator.reprint(listCreator.pretty_list(1))
time.sleep(1)
listCreator.reprint(listCreator.pretty_list(2))
'''
