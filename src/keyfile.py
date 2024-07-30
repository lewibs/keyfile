import argparse
from argparse import Namespace
from Parsers import get_lines_from_keyfile, get_tokens_from_lines

def parse_args() -> Namespace:
    # Create the argument parser
    parser = argparse.ArgumentParser(description="TODO this is for -h")
    
    # Add an argument for user input
    parser.add_argument("-kf", type=str, help="target keyfile location")
    
    # Parse the arguments
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    args.kf = "C:/Users/lewibs/github/keyfile/examples/lewibs.planck.ez.glow.kf"
    # having to go through the code again and again causes xO(n) which could easily be improved.
    # however, the cleanness of this code will suffer and since it is unlikly that the .kfs will be that long, i think its safe to keep it slow
    lines = get_lines_from_keyfile(args.kf)
    tokens = get_tokens_from_lines(lines, injected=False)

    print(tokens)

if __name__ == "__main__":
    main()
