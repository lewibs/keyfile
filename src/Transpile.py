from Parsers import Token
from env import PATH
import os

def write_to_c(path:str, sentences)->None:
    # Read the template C file
    with open(os.path.join(PATH, "misc", 'keymap.template.c'), 'r') as file:
        c_code = file.read()

    keycodes = "\tNO_CODE=SAFE_RANGE"
    layout = ""
    layers = ""
    ledmap = ""
    keymap_cols = ""
    keymap_rows = ""
    dual_keys = ""

    for sentence in sentences:
        if sentence.type == Token.LAYER:
            layer, keys, colors = 1, 2, 3
            layout += f"\t[{layer}] = {keys},\n"
            ledmap += f"\t[{layer}] = {colors},\n"
            layers += f"\t{layer},\n"
        if sentence.type == Token.KEYBOARD:
            keymap_cols = str(sentence.cols())
            keymap_rows = str(sentence.rows())
  
    layout = layout[:-2]
    ledmap = ledmap[:-2]
    layers = layers[:-2]

    c_code = c_code.replace('KEYCODES_INSERTION_POINT', keycodes)
    c_code = c_code.replace('LAYER_INSERTION_POINT', layers)
    c_code = c_code.replace('LAYOUT_INSERTION_POINT', layout)
    c_code = c_code.replace('LEDMAP_INSERTION_POINT', ledmap)
    c_code = c_code.replace("ROW_INSERTION_POINT", keymap_rows)
    c_code = c_code.replace("COL_INSERTION_POINT", keymap_cols)
    
    with open(os.path.join(path, 'keymap.c'), 'w') as file:
        file.write(c_code)