import argparse
from argparse import Namespace
from Parsers import parse_keyfile
from Exceptions import ERROR_STACK, ParserException
from Transpile import write_to_c
import os
from env import TEMPDIR

def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description="See documentation for more details: https://github.com/lewibs/keyfile")
    
    # Add arguments
    parser.add_argument("-i", "--keyfile", type=str, required=True, help="Target input keyfile location")
    parser.add_argument("-n", "--name", type=str, default="keyboard", help="Keyboard name")
    parser.add_argument("-o", "--output", type=str, default=os.getcwd(), help="Target directory for output to be saved")
    parser.add_argument("-l", "--linked", action="store_true", help="Saves the linked .kf")
    parser.add_argument("-m", "--keymap", action="store_true", help="Saves the transpiled keymap files")
    
    args = parser.parse_args()
    args.output = os.path.join(args.output, args.name)

    return args

def get_sentences_from_keyfile(kf:str):
    sentences = []
    try:
        sentences = parse_keyfile(kf)
    except ParserException as e:
        ERROR_STACK.insert(0, "Most recent call is lowest")
        ERROR_STACK.insert(0, str(e)+"\n")

        for string in reversed(ERROR_STACK):
            print(string)
    except Exception as e:
        print("UNEXPECTED_ERROR: Ran into an unexpected issue. This is most likely not an issue with your code. This error occured while parsing the keyfile")
        raise e


    return sentences

def write_sentences_to_linked_file(args, sentences):
    try:
        if args.linked:
            with open(os.path.join(args.output,"linked.kf"), 'w') as file:
                # Iterate over each sentence and write it to the file
                for sentence in sentences:
                    file.write(" ".join(sentence.words) + '\n')  # Ensure each sentence is on a new line
    except Exception as e:
        print("UNEXPECTED_ERROR: Ran into an unexpected issue. This is most likely not an issue with your code. This error occured while writing to the linked keyfile")


def main() -> None:
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    # having to go through the code again and again causes xO(n) which could easily be improved.
    # however, the cleanness of this code will suffer and since it is unlikly that the .kfs will be that long, i think its safe to keep it slow
    sentences = get_sentences_from_keyfile(args.keyfile)
    write_sentences_to_linked_file(args, sentences)
    write_to_c(args.output, sentences)


if __name__ == "__main__":
    main()
