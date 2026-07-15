# Repository: https://github.com/Efrat328/Kung-Fu-Chess
import sys
from board import Board, BoardParseError
from input_parser import InputParser
from game import Game


def main():
    raw_text = sys.stdin.read()
    board = InputParser.parse(raw_text)

    try:
        board.validate()
    except BoardParseError as e:
        print(f"ERROR {e.error_code}")
        return

    commands = InputParser.parse_commands(raw_text)
    game = Game(board)
    output_lines = []

    for command in commands:
        tokens = command.split()
        verb = tokens[0]

        if verb == "click":
            x, y = int(tokens[1]), int(tokens[2])
            game.handle_click(x, y)
        elif verb == "jump":
            x, y = int(tokens[1]), int(tokens[2])
            game.handle_jump(x, y)
        elif verb == "wait":
            ms = int(tokens[1])
            game.advance_clock(ms)
        elif verb == "print" and tokens[1] == "board":
            output_lines.append(game.get_board_output())

    if output_lines:
        print("\n".join(output_lines))


if __name__ == "__main__":
    main()