#include QMK_KEYBOARD_H
#include "eeprom.h"

extern rgb_config_t rgb_matrix_config;

enum keycodes {
KEYCODES_INSERTION_POINT
};

enum layers {
LAYER_INSERTION_POINT
};

const uint16_t PROGMEM keymaps[][ROW_INSERTION_POINT][COL_INSERTION_POINT] = {
LAYOUT_INSERTION_POINT
};


const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT][3] = {
LEDMAP_INSERTION_POINT
};

uint8_t layer_state_set_user(uint8_t state) {
DUALKEY_INSERTION_POINT
return state
};

/**
 * This sets the colors based on the active layer
 */
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