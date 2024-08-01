from Parsers import Token, GlobalDefinitions
from env import PATH
import os
from Parsers import SENTENCES

class C_Segment:
    def __init__(self, init):
        self.code = init
        self.lines = 0

    def add_code(self, code, newline=True):
        self.code += code
        if newline:
            self.lines += 1

    def add_line(self, val):
        self.add_code(f"\t{val};\n")

    def __str__(self) -> str:
        return self.code
    
class C_Enum(C_Segment):
    def __init__(self, name, INIT=None):
        super().__init__(f"enum {name} = " + "{\n")
        if INIT:
            self.add_code(f"\t{name}={INIT}")

    def add_line(self, val):
        self.add_code(f"\t{val},\n")

    def close(self):
        self.code = self.code[:-2]
        self.add_code("\n};")

class C_List(C_Segment):
    def __init__(self, type, name):
        code = f"const {type} PROGMEM {name}[]"
        super().__init__(code)

    def set_dims(self, rows, cols):
        self.add_code(f"[{rows}][{cols}]" + " = {\n", newline=False)

    def add_line(self, name):
        line = f"\t[{name}] = " + "{"

        if self.lines == 0:
            self.add_code(line)
        else:
            self.add_code(",\n" + line)

    def add_row(self, items):
        self.add_code("{")
        for item in items:
            self.add_code(str(item) + ",")
        self.code = self.code[:-1]
        self.add_code("},")

    def close_line(self):
        self.code = self.code[:-1]
        self.add_code("}")

    def close(self):
        self.add_code("\n};")

class C_Func(C_Segment):
    def __init__(self, type, name, inputs):
        super().__init__(f"{type} {name}({" ".join(inputs)})" + "{\n")
    def ret(self, ret):
        self.add_code(f"\treturn {ret}")
        self.add_code("\n};")

class C_Head(C_Segment):
    def __init__(self):
        super().__init__("")

    def add_line(self, val):
        self.add_code(f"{val};\n")

    def include(self, val):
        self.add_code(f"#include {val}\n")

RGB_MATRIX_FUNCTION = """
bool rgb_matrix_indicators_user(void) {
  int layer = biton32(layer_state);

  for (int i = 0; i < RGB_MATRIX_LED_COUNT; i++) {
    HSV hsv = {
      .h = pgm_read_byte(&ledmap[layer][i][0]),
      .s = pgm_read_byte(&ledmap[layer][i][1]),
      .v = pgm_read_byte(&ledmap[layer][i][2]),
    };
    if (!hsv.h && !hsv.s && !hsv.v) {
        rgb_matrix_set_color( i, 0, 0, 0 );
    } else {
        RGB rgb = hsv_to_rgb( hsv );
        float f = (float)rgb_matrix_config.hsv.v / UINT8_MAX;
        rgb_matrix_set_color( i, f * rgb.r, f * rgb.g, f * rgb.b );
    }
  }

  return true;
};
"""

def write_to_c(path:str, sentences)->None:
    # Read the template C file
    with open(os.path.join(PATH, "misc", 'keymap.template.c'), 'r') as file:
        c_code = file.read()

    headers = C_Head()
    headers.include("QMK_KEYBOARD_H")
    headers.include('"eeprom.h"')
    headers.add_line("extern rgb_config_t rgb_matrix_config")
    rgb_shaders = C_Segment(RGB_MATRIX_FUNCTION)

    keycodes = C_Enum("keycodes", "SAFE_RANGE")
    layers = C_Enum("layers")
    keymap = C_List("uint16_t", "keymap")
    ledmap = C_List("uint8_t", "ledmap")
    dualkeys = C_Func("uint8_t", "layer_state_set_user", ["uint8_t", "state"])
     
    #TODO remove this
    rows=0
    cols=0

    for sentence in sentences:
        if sentence.type == Token.LAYER:
            name = sentence.words[1]
            keys = sentence.words[2:]

            keymap.add_line(name)
            #TODO make this ref the variable for items in the row
            codes = [SENTENCES[key].translate_code() for key in keys]
            for row in range(0, len(codes), cols):
                keymap.add_row(codes[row:row+cols])
            keymap.close_line()
            
            ledmap.add_line(name)
            colors = [SENTENCES[key].translate_color() for key in keys]
            for color in colors:
                ledmap.add_row(color)
            ledmap.close_line()
        
        if sentence.type == Token.KEYBOARD:
            rows = int(sentence.words[2])
            cols = int(sentence.words[3])
            keymap.set_dims(sentence.words[2], sentence.words[3])
            [layers.add_line(word) for word in sentence.words[4:]]
            ledmap.set_dims(str(rows*cols), 3)
        if sentence.type == Token.KEY and sentence.words[1].startswith(GlobalDefinitions.DUAL):
            dualkeys.add_line(f"state = update_tri_layer_state(state, {sentence.words[2]}, {sentence.words[3]}, {sentence.words[4]})")

    keycodes.close()
    layers.close()
    keymap.close()
    ledmap.close()
    dualkeys.ret("state")

    c_code = ""

    for seg in [headers, keycodes, layers, keymap, ledmap, dualkeys, rgb_shaders]:
        c_code += "\n" + str(seg)

    with open(os.path.join(path, 'keymap.c'), 'w') as file:
        file.write(c_code)