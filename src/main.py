import sys
from board import Board, BoardParseError
from input_parser import InputParser


def main():
    raw_text = sys.stdin.read()
    board = InputParser.parse(raw_text)
    
    try:
        board.validate()
        print(board.to_canonical_string())
    except BoardParseError as e:
        print(f"ERROR {e.error_code}")


if __name__ == "__main__":
    main()