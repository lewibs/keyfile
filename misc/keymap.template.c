#include QMK_KEYBOARD_H
#include "eeprom.h"

//NOTE: these can be used for inplace modifications
// uint8_t keymap_layer_count(void);
// uint16_t keycode_at_keymap_location(uint8_t layer_num, uint8_t row, uint8_t column);

extern rgb_config_t rgb_matrix_config;

enum keycodes {
//KEYCODES_INSERTION_POINT
};

enum layers {
//LAYER_INSERTION_POINT
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
//LAYOUT_INSERTION_POINT
};


const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT+1][3] = {
//LEDMAP_INSERTION_POINT
};

//THIS IS NEEDED FOR SETTING THE COLOR BASED ON THE LAYER
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
}

//THIS IS NEEDED for double layers
uint8_t layer_state_set_user(uint8_t state) {
  //TODO figure out how to insert here
  //return update_tri_layer_state(state, _LOWER, _RAISE, _ADJUST);
  return 0
}