from Tokens import BaseToken, LayerToken
from Parsers import TOKENS
from typing import List
from Files import get_tmp_dir
from env import PATH
import os

def create_c_file(path:str, tokens:List[BaseToken])->None:
    # Read the template C file
    with open(os.path.join(PATH, "misc", 'keymap.template.c'), 'r') as file:
        c_code = file.read()

    keycodes = "\tNO_CODE=SAFE_RANGE"
    layout = ""
    layers = ""
    ledmap = ""

    for token in reversed(tokens):
        if not isinstance(token, LayerToken):
            break

        layer, keys, colors = token.transpile(TOKENS)
        layout += f"\t[{layer}] = {keys},\n"
        ledmap += f"\t[{layer}] = {colors},\n"
        layers += f"\t{layer},\n"
    
    layout = layout[:-2]
    ledmap = ledmap[:-2]
    layers = layers[:-2]

    c_code = c_code.replace('//KEYCODES_INSERTION_POINT', keycodes)
    c_code = c_code.replace('//LAYER_INSERTION_POINT', layers)
    c_code = c_code.replace('//LAYOUT_INSERTION_POINT', layout)
    c_code = c_code.replace('//LEDMAP_INSERTION_POINT', ledmap)
    
    # Write the generated C code to a new file
    with open(os.path.join(path, 'keymap.c'), 'w') as file:
        file.write(c_code)