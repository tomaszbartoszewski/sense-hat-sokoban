import copy
#from enum import IntFlag
from time import sleep

# I tried to use enum here, but I was having a problem with packages in the image, so I gave up as I just want to get it done
class FieldValue:
    Empty = 0
    Wall = 1
    Player = 2
    Box = 4
    Goal = 8


def mapStringToBoardRow(line):
    field_map = {
        '#': FieldValue.Wall,
        '@': FieldValue.Player,
        '+': (FieldValue.Player | FieldValue.Goal),
        '$': FieldValue.Box,
        '*': (FieldValue.Box | FieldValue.Goal),
        '.': FieldValue.Goal,
        ' ': FieldValue.Empty
    }
    row = []
    for cell in line:
        row.append(field_map[cell])

    return row


def get_levels():
    board_definition = open('BoardDefinition.txt', 'r')

    levels = []
    board = []
    number_of_rows = 0

    for line in board_definition.read().splitlines():
        if number_of_rows == 0:
            if len(board) > 0:
                levels.append(board)
                board = []
            number_of_rows = int(line)
        else:
            board.append(mapStringToBoardRow(line))
            number_of_rows -= 1
    levels.append(board)

    return levels


def print_to_console(level):
    field_to_console_map = {
        FieldValue.Wall: '#',
        FieldValue.Player: '@',
        FieldValue.Player | FieldValue.Goal: '+',
        FieldValue.Box: '$',
        FieldValue.Box | FieldValue.Goal: '*',
        FieldValue.Goal: '.',
        FieldValue.Empty: ' '
    }
    for row in level:
        for cell in row:
            print(field_to_console_map[cell], end='')
        print()

from sense_hat import SenseHat

sense = SenseHat()

def print_to_senseHAT(level):
    field_to_colour_map = {
        FieldValue.Wall: (204, 4, 4),
        FieldValue.Player: (1, 158, 1),
        FieldValue.Player | FieldValue.Goal: (1, 158, 1),
        FieldValue.Box: (112, 114, 112),
        FieldValue.Box | FieldValue.Goal: (19, 20, 19),
        FieldValue.Goal: (13, 0, 198),
        FieldValue.Empty: (0, 0, 0)
    }
    sense.clear()
    for row_index, row in enumerate(level):
        for column_index, cell in enumerate(row):
            sense.set_pixel(row_index, column_index, field_to_colour_map[cell])


def play_level(level):
    #print_to_console(level)
    print_to_senseHAT(level)


def main():
    levels = get_levels()
    for level in levels:
        play_level(copy.deepcopy(level))
        sleep(1)


if __name__ == '__main__':
    main()
