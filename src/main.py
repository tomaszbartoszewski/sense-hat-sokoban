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
            print(level)
            sense.set_pixel(column_index, row_index, field_to_colour_map[cell])


def can_move(level, destination, behind):
    (dest_x, dest_y) = destination
    destination_value = level[dest_y][dest_x]
    if destination_value == FieldValue.Wall:
        return False
    (behind_x, behind_y) = behind
    behind_value = level[behind_y][behind_x]
    if destination_value & FieldValue.Box == FieldValue.Box and (
            behind_value & FieldValue.Box == FieldValue.Box or behind_value & FieldValue.Wall == FieldValue.Wall):
        return False
    return True


def get_player_position(level):
    for row_index, row in enumerate(level):
        for column_index, cell in enumerate(row):
            if cell & FieldValue.Player == FieldValue.Player:
                return column_index, row_index


def try_move(level, player_position, destination, behind):
    if can_move(level, destination, behind):
        level[player_position[1]][player_position[0]] & ~FieldValue.Player
        level[destination[1]][destination[0]] & ~FieldValue.Box
        level[behind[1]][behind[0]] & FieldValue.Box
        return True
    return False


def play_level(level):
    current_state = copy.deepcopy(level)
    (position_x, position_y) = get_player_position(current_state)
    board_changed = True
    while True:
        if board_changed:
            board_changed = False
            print_to_senseHAT(level)
        for event in sense.stick.get_events():
            print("The joystick was {} {}".format(event.action, event.direction))
            if event.action == "pressed":
                if event.direction == "middle":
                    current_state = copy.deepcopy(level)
                    (position_x, position_y) = get_player_position(current_state)
                    board_changed = True
                elif event.direction == "up":
                    board_changed = try_move(current_state, (position_x, position_y), (position_x, position_y - 1),
                                             (position_x, position_y - 2))
                elif event.direction == "down":
                    board_changed = try_move(current_state, (position_x, position_y), (position_x, position_y + 1),
                                             (position_x, position_y + 2))
                elif event.direction == "left":
                    board_changed = try_move(current_state, (position_x, position_y), (position_x - 1, position_y),
                                             (position_x - 2, position_y))
                elif event.direction == "right":
                    board_changed = try_move(current_state, (position_x, position_y), (position_x + 1, position_y),
                                             (position_x + 2, position_y))


def main():
    levels = get_levels()
    for level in levels:
        play_level(copy.deepcopy(level))
        sleep(1)


if __name__ == '__main__':
    main()
