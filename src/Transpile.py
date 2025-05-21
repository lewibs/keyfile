
from Parsers import Token, GlobalDefinitions, SENTENCES
from Exceptions import ParserException
import os

def write_to_c(path:str, sentences) -> None:
    MACROS = """
bool process_record_user(uint16_t keycode, keyrecord_t *record) {
  switch (keycode) {
    case DUMMY_INIT_VAL:
        return true;
INSERT_MASK_MACROS
INSERT_MACROS
  }
  return true;
}
"""

    def make_send_string_macro(code, string, delay):
        OPEN = "{"
        CLOSE = "}"
        return f'''
    case {code}:
        if (record->event.pressed) {OPEN}
            SEND_STRING_DELAY("{string}", {delay});
        {CLOSE}
        break;
'''

    def make_layer_mask_macro(code, masks):
        OPEN = "{"
        CLOSE = "}"
        on_lines = "\n            ".join([f"layer_on({mask});" for mask in masks])
        off_lines = "\n            ".join([f"layer_off({mask});" for mask in reversed(masks)])
    
        return f'''
    case {code}:
        if (record->event.pressed) {OPEN}
            {on_lines}
        {CLOSE} else {OPEN}
            {off_lines}
        {CLOSE}
        return false;
        break;
'''

    CONFIG = """
#pragma once

#ifdef AUDIO_ENABLE
#define STARTUP_SONG SONG(PLANCK_SOUND)
#endif

#define MIDI_BASIC

#define ENCODER_RESOLUTION 4

/*
  Set any config.h overrides for your specific keymap here.
  See config.h options at https://docs.qmk.fm/#/config_options?id=the-configh-file
*/

#define ORYX_CONFIGURATOR
#undef DEBOUNCE
#define DEBOUNCE 10

#define USB_SUSPEND_WAKEUP_DELAY 0
#undef MOUSEKEY_TIME_TO_MAX
#define MOUSEKEY_TIME_TO_MAX 40
#undef MOUSEKEY_MAX_SPEED
#define MOUSEKEY_MAX_SPEED 5

#define FIRMWARE_VERSION u8"rlj79/RLPW6"
#define RAW_USAGE_PAGE 0xFF60
#define RAW_USAGE_ID 0x61
#define LAYER_STATE_LAYER_COUNTBIT

#define RGB_MATRIX_STARTUP_SPD 60
"""

    HEADER = """
#include QMK_KEYBOARD_H
#include "eeprom.h"

extern rgb_config_t rgb_matrix_config;
"""

    KEY_CODES = """
enum keycodes {
INSERT_KEY_CODES
};
"""

    LAYER_NAMES = """
enum layers {
INSERT_LAYER_NAMES
};
"""

    KEY_MAP = """
const uint16_t PROGMEM keymaps[][INSERT_ROWS][INSERT_COLS] = {
INSERT_KEY_LAYER
};
"""

    def create_key_map_layer(string, layer, macro, entries):
        return string + f"[{layer}] = {macro}({','.join(entries)}),\n"

    LED_MAP = """
const uint8_t PROGMEM ledmap[][INSERT_LED_COUNT][3] = {
INSERT_LED_LAYER
};
"""

    def create_led_map_layer(string, layer, colors):
        return string + f"[{layer}] = " + "{" + ",".join(colors) + "},\n"

    COMBO_LAYERS = """
uintLAYER_COUNT_t layer_state_set_user(uintLAYER_COUNT_t state) {
INSERT_COMBO_LAYER

return state;
}
"""

    def create_combo_layer(target_layer, layers):
        condition = " && ".join([f"layer_state_cmp(state, {layer})" for layer in layers])
        return f"""\
bool {target_layer}_is_on = {condition};
if ({target_layer}_is_on) {{
    state |= (1<<{target_layer});
}} else {{
    state &= ~(1<<{target_layer});
}}
"""

    RGB_MATRIX_FUNCTION = """
void keyboard_post_init_user(void) {
  rgb_matrix_enable();
}

bool rgb_matrix_indicators_user(void) {
  int layer = biton32(layer_state);

  for (int i = 0; i < INSERT_LED_COUNT; i++) {
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

    LED_INJECTABLE = ""
    KEY_INJECTABLE = ""
    COMBO_INJECTABLE = ""
    KEY_CODE_INJECTABLE = "DUMMY_INIT_VAL = SAFE_RANGE,\n"
    MACRO_INJECTABLE = ""
    LAYER_MASK_INJECTABLE = ""


    for sentence in sentences:
        if sentence.type == Token.KEYBOARD:
            KEY_MAP = KEY_MAP.replace("INSERT_ROWS", sentence.rows())
            KEY_MAP = KEY_MAP.replace("INSERT_COLS", sentence.cols())
            LED_MAP = LED_MAP.replace("INSERT_LED_COUNT", sentence.leds())
            RGB_MATRIX_FUNCTION = RGB_MATRIX_FUNCTION.replace("INSERT_LED_COUNT", sentence.leds())
            LAYER_NAMES = LAYER_NAMES.replace("INSERT_LAYER_NAMES", ",\n".join(sentence.layers()))
            layer_count = len(sentence.layers())
            layer_count = 8 if layer_count < 8 else 16 if layer_count < 16 else 32 if layer_count < 32 else -1
            if layer_count == -1:
                raise ParserException("Max Layers: 32 is the maximum amount of layers")
            CONFIG = CONFIG.replace("LAYER_COUNT", str(layer_count))
            COMBO_LAYERS = COMBO_LAYERS.replace("LAYER_COUNT", str(layer_count))
            MACRO = sentence.macro()
        elif sentence.type == Token.LAYER:
            keys = sentence.keys()
            colors = sentence.leds()
            layer_name = sentence.name()

            KEY_INJECTABLE = create_key_map_layer(KEY_INJECTABLE, layer_name, MACRO, keys)
            LED_INJECTABLE = create_led_map_layer(LED_INJECTABLE, layer_name, colors)
        elif sentence.type == Token.KEY:
            if sentence.key_type() == GlobalDefinitions.COMBO:
                layers = sentence.layers()
                COMBO_INJECTABLE += create_combo_layer(layers[-1], layers[:-1]) + "\n"
            elif sentence.key_type() == GlobalDefinitions.MASK:
                KEY_CODE_INJECTABLE += f"{sentence.name()},\n"
                LAYER_MASK_INJECTABLE += make_layer_mask_macro(sentence.name(), sentence.masks())
            elif sentence.key_type() == GlobalDefinitions.MACRO:
                KEY_CODE_INJECTABLE += f"{sentence.name()},\n"
                MACRO_INJECTABLE += make_send_string_macro(sentence.name(), sentence.string(), 40) 


   

    #trim comma
    LED_INJECTABLE = LED_INJECTABLE[:-2]
    KEY_INJECTABLE = KEY_INJECTABLE[:-2]
    KEY_CODE_INJECTABLE = KEY_CODE_INJECTABLE[:-2]
    COMBO_INJECTABLE = COMBO_INJECTABLE[:-1]

    LED_MAP = LED_MAP.replace("INSERT_LED_LAYER", LED_INJECTABLE)
    KEY_MAP = KEY_MAP.replace("INSERT_KEY_LAYER", KEY_INJECTABLE)
    COMBO_LAYERS = COMBO_LAYERS.replace("INSERT_COMBO_LAYER", COMBO_INJECTABLE)
    KEY_CODES = KEY_CODES.replace("INSERT_KEY_CODES", KEY_CODE_INJECTABLE)
    MACROS = MACROS.replace("INSERT_MACROS", MACRO_INJECTABLE)
    MACROS = MACROS.replace("INSERT_MASK_MACROS", LAYER_MASK_INJECTABLE)

    c_code = f"{HEADER}{KEY_CODES}{LAYER_NAMES}{KEY_MAP}{LED_MAP}{COMBO_LAYERS}{RGB_MATRIX_FUNCTION}{MACROS}"

    with open(os.path.join(path, 'keymap.c'), 'w') as file:
        file.write(c_code)

    with open(os.path.join(path, 'config.h'), 'w') as file:
        file.write(CONFIG)
