import argparse
from argparse import Namespace
from Parsers import get_lines_from_keyfile, get_tokens_from_lines
from Tokens import BaseToken
from typing import List
from Files import clean_tmp_dir, move_directory, get_tmp_dir
from Transpile import create_c_file

def parse_args() -> Namespace:
    # Create the argument parser
    parser = argparse.ArgumentParser(description="TODO this is for -h")
    
    # Add an argument for user input
    parser.add_argument("-kf", type=str, help="target keyfile location")

    parser.add_argument("-kf_resolved", type=str, help="target location for the dependency resolution info")
    
    parser.add_argument("-km", type=str, help="target location for the keymap files that are created")

    # Parse the arguments
    return parser.parse_args()

def write_resolved_tokens(to:str, tokens:List[BaseToken]):
    with open(to, 'w') as file:
        for token in tokens:
            file.write(f"{str(token)}\n")

def main() -> None:
    args = parse_args()
    args.kf = "C:/Users/lewibs/github/keyfile/examples/lewibs.planck.ez.glow.kf"
    # having to go through the code again and again causes xO(n) which could easily be improved.
    # however, the cleanness of this code will suffer and since it is unlikly that the .kfs will be that long, i think its safe to keep it slow
    lines = get_lines_from_keyfile(args.kf)
    tokens = get_tokens_from_lines(lines, injected=False)
    kb_name = args.kf.split("/")[-1][:-3] 

    if args.kf_resolved:
        write_resolved_tokens(args.kf_resolved, tokens)

    path = get_tmp_dir(kb_name)

    create_c_file(path, tokens)

    if args.km:
        move_directory(path, args.km)

    #TODO make bin here...

    clean_tmp_dir(path)


if __name__ == "__main__":
    main()
