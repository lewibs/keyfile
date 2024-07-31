#include QMK_KEYBOARD_H
#include "eeprom.h"

//NOTE: these can be used for inplace modifications
// uint8_t keymap_layer_count(void);
// uint16_t keycode_at_keymap_location(uint8_t layer_num, uint8_t row, uint8_t column);

extern rgb_config_t rgb_matrix_config;

enum keycodes {
	NO_CODE=SAFE_RANGE
};

enum layers {
	_BASE,
	_FN,
	_MOUSE,
	_DELETE,
	_NUMS,
	_SYMS
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
	[_BASE] = LAYOUT_planck_grid(KC_Q,KC_W,KC_E,KC_R,KC_T,KC_DELETE,KC_BSPC,KC_Y,KC_U,KC_I,KC_O,KC_P,KC_A,KC_S,KC_D,KC_F,KC_G,KC_QUOTE,KC_ENTER,KC_H,KC_J,KC_K,KC_L,KC_SCLN,KC_Z,KC_X,KC_C,KC_V,KC_B,KC_ESCAPE,KC_TAB,KC_N,KC_M,KC_COMMA,KC_DOT,KC_SLASH,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_FN),KC_LSFT,MO(_SYMS),KC_SPACE,KC_NO,MO(_NUMS),MO(_MOUSE),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
	[_FN] = LAYOUT_planck_grid(KC_F1,KC_F2,KC_F3,KC_F4,KC_F5,KC_F6,KC_F7,KC_F8,KC_F9,KC_F10,KC_F11,KC_F12,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_BRIGHTNESS_DOWN,KC_BRIGHTNESS_UP,KC_AUDIO_VOL_DOWN,KC_AUDIO_VOL_UP,KC_NO,KC_AUDIO_MUTE,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_MEDIA_PLAY_PAUSE,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT),
	[_MOUSE] = LAYOUT_planck_grid(KC_NO,KC_MS_BTN2,KC_MS_UP,KC_MS_BTN1,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_ENTER,KC_UP,KC_NO,KC_NO,KC_NO,KC_MS_LEFT,KC_MS_DOWN,KC_MS_RIGHT,KC_NO,KC_NO,KC_TRANSPARENT,LCTL(KC_LEFT),KC_LEFT,KC_DOWN,KC_RIGHT,RCTL(KC_RIGHT),KC_MS_WH_LEFT,KC_MS_WH_UP,KC_NO,KC_MS_WH_DOWN,KC_MS_WH_RIGHT,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_HOME,KC_NO,KC_END,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT),
	[_DELETE] = LAYOUT_planck_grid(KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,LCTL(LSFT(KC_DELETE)),KC_TAB,LCTL(KC_DELETE),KC_DELETE,KC_NO,KC_NO,KC_TRANSPARENT,KC_NO,KC_BSPC,LCTL(KC_BSPC),KC_ENTER,LCTL(LSFT(KC_BSPC)),KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT),
	[_NUMS] = LAYOUT_planck_grid(KC_0,KC_1,KC_2,KC_3,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_PERC,KC_TILD,KC_BSLS,KC_NO,KC_DOT,KC_4,KC_5,KC_6,KC_NO,KC_GRAVE,KC_TRANSPARENT,KC_NO,KC_MINUS,KC_PLUS,KC_SLASH,KC_ASTR,KC_EQUAL,KC_7,KC_8,KC_9,KC_NO,KC_CALCULATOR,KC_TRANSPARENT,KC_NO,KC_NO,KC_LABK,KC_RABK,KC_CIRC,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT),
	[_SYMS] = LAYOUT_planck_grid(KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_EXLM,KC_LCBR,KC_RCBR,KC_AT,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_GRAVE,KC_TRANSPARENT,KC_NO,KC_HASH,KC_LPRN,KC_RPRN,KC_DLR,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_TRANSPARENT,KC_TRANSPARENT,KC_NO,KC_PIPE,KC_LBRC,KC_RBRC,KC_AMPR,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT,KC_TRANSPARENT)
};


const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT+1][3] = {
	[_BASE] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
	[_FN] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
	[_MOUSE] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
	[_DELETE] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
	[_NUMS] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
	[_SYMS] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}
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