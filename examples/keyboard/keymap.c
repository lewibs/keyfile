
#include QMK_KEYBOARD_H
#include "eeprom.h"

extern rgb_config_t rgb_matrix_config;

enum keycodes {
RGB_SLD = SAFE_RANGE
};

enum layers {
_base,
_syms,
_nums,
_delete,
_mouse,
_fn
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
[_base] = LAYOUT_planck_grid(KC_Q,KC_W,KC_E,KC_R,KC_T,KC_DELETE,KC_BSPC,KC_Y,KC_U,KC_I,KC_O,KC_P,KC_A,KC_S,KC_D,KC_F,KC_G,KC_QUOTE,KC_ENTER,KC_H,KC_J,KC_K,KC_L,KC_SCLN,KC_Z,KC_X,KC_C,KC_V,KC_B,KC_ESCAPE,KC_TAB,KC_N,KC_M,KC_COMMA,KC_DOT,KC_SLASH,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
[_syms] = LAYOUT_planck_grid(KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_DELETE,KC_BSPC,KC_NO,KC_EXLM,KC_LCBR,KC_RCBR,KC_AT,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_QUOTE,KC_ENTER,KC_NO,KC_HASH,KC_LPRN,KC_RPRN,KC_DLR,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_ESCAPE,KC_TAB,KC_NO,KC_PIPE,KC_LBRC,KC_RBRC,KC_AMPR,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
[_nums] = LAYOUT_planck_grid(KC_0,KC_1,KC_2,KC_3,KC_NO,KC_DELETE,KC_BSPC,KC_NO,KC_PERC,KC_TILD,KC_BSLS,KC_NO,KC_DOT,KC_4,KC_5,KC_6,KC_NO,KC_QUOTE,KC_ENTER,KC_NO,KC_MINUS,KC_PLUS,KC_SLASH,KC_ASTR,KC_EQUAL,KC_7,KC_8,KC_9,KC_NO,KC_CALCULATOR,KC_TAB,KC_NO,KC_NO,KC_LABK,KC_RABK,KC_CIRC,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
[_delete] = LAYOUT_planck_grid(KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_DELETE,KC_BSPC,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,LCTL(LSFT(KC_DELETE)),KC_TAB,LCTL(KC_DELETE),KC_DELETE,KC_NO,KC_NO,KC_ENTER,KC_NO,KC_BSPC,LCTL(KC_BSPC),KC_ENTER,LCTL(LSFT(KC_BSPC)),KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_ESCAPE,KC_TAB,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
[_mouse] = LAYOUT_planck_grid(KC_NO,KC_MS_BTN2,KC_MS_UP,KC_MS_BTN1,KC_NO,KC_DELETE,KC_BSPC,KC_NO,KC_ENTER,KC_UP,KC_NO,KC_NO,KC_NO,KC_MS_LEFT,KC_MS_DOWN,KC_MS_RIGHT,KC_NO,KC_NO,KC_ENTER,LCTL(KC_LEFT),KC_LEFT,KC_DOWN,KC_RIGHT,RCTL(KC_RIGHT),KC_MS_WH_LEFT,KC_MS_WH_UP,KC_NO,KC_MS_WH_DOWN,KC_MS_WH_RIGHT,KC_ESCAPE,KC_TAB,KC_NO,KC_HOME,KC_NO,KC_END,KC_NO,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT),
[_fn] = LAYOUT_planck_grid(KC_F1,KC_F2,KC_F3,KC_F4,KC_F5,KC_F6,KC_F7,KC_F8,KC_F9,KC_F10,KC_F11,KC_F12,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_BRIGHTNESS_DOWN,KC_BRIGHTNESS_UP,KC_AUDIO_VOL_DOWN,KC_AUDIO_VOL_UP,KC_NO,KC_AUDIO_MUTE,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_NO,KC_MEDIA_PLAY_PAUSE,KC_LEFT_CTRL,KC_LEFT_ALT,MO(_fn),KC_LSFT,MO(_syms),KC_SPACE,KC_NO,MO(_nums),MO(_mouse),KC_NO,KC_LEFT_GUI,KC_LEFT_ALT)
};

const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT][3] = {
[_base] = {{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,255,255},{0,255,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{180,255,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{180,255,255},{180,255,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}},
[_syms] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,255,255},{0,255,255},{0,0,0},{210,255,255},{0,0,255},{0,0,255},{170,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,255},{180,255,255},{0,0,0},{170,255,255},{0,0,255},{0,0,255},{0,0,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{180,255,255},{180,255,255},{0,0,0},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}},
[_nums] = {{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,0},{0,255,255},{0,255,255},{0,0,0},{170,255,255},{0,0,255},{0,0,255},{0,0,0},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,0},{0,0,255},{180,255,255},{0,0,0},{0,0,255},{85,255,255},{0,0,255},{85,255,255},{0,0,255},{0,0,255},{0,0,255},{0,0,255},{0,0,0},{170,255,255},{180,255,255},{0,0,0},{0,0,0},{0,0,255},{0,0,255},{85,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}},
[_delete] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,255,255},{0,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,255,255},{180,255,255},{0,255,255},{0,255,255},{0,0,0},{0,0,0},{180,255,255},{0,0,0},{0,255,255},{0,255,255},{180,255,255},{0,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{180,255,255},{180,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}},
[_mouse] = {{0,0,0},{21,255,255},{210,255,255},{21,255,255},{0,0,0},{0,255,255},{0,255,255},{0,0,0},{180,255,255},{210,255,255},{0,0,0},{0,0,0},{0,0,0},{210,255,255},{210,255,255},{210,255,255},{0,0,0},{0,0,0},{180,255,255},{210,255,255},{210,255,255},{210,255,255},{210,255,255},{210,255,255},{210,255,255},{210,255,255},{0,0,0},{210,255,255},{210,255,255},{180,255,255},{180,255,255},{0,0,0},{210,255,255},{0,0,0},{210,255,255},{0,0,0},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}},
[_fn] = {{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{170,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,255,255},{85,255,255},{0,255,255},{85,255,255},{0,0,0},{0,255,255},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{43,255,255},{0,0,255},{43,255,255},{43,255,255},{0,0,0},{43,255,255},{43,255,255}}
};

uint8_t layer_state_set_user(uint8_t state) {
state = update_tri_layer_state(state, _syms, _nums, _delete);
return state;
}

void keyboard_post_init_user(void) {
  rgb_matrix_enable();
}

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
