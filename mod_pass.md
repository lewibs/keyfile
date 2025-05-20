
#include “quantum.h”

// ——— Layer Definitions ——————————————————————————————
enum layers {
    _BASE,
    _MOD,
};

// ——— Custom Keycodes ———————————————————————————————
enum custom_keycodes {
    MOD_PASS = SAFE_RANGE,
};

// ——— Helper: find first non-transparent key below current layer ———
uint16_t get_lower_layer_key(uint8_t row, uint8_t col, uint8_t current_layer) {
    // iterate down through layers beneath current
    for (int8_t layer = current_layer - 1; layer >= 0; layer--) {
        if (layer_state_is(layer)) {
            uint16_t kc = pgm_read_word(&keymaps[layer][row][col]);
            if (kc != KC_TRNS) {
                return kc;
            }
        }
    }
    // fallback: no key found
    return KC_NO;
}

// ——— process_record_user: handle MOD_PASS ———————————————
bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (keycode == MOD_PASS && record->event.pressed) {
        uint8_t row = record->event.key.row;
        uint8_t col = record->event.key.col;

        uint16_t target = get_lower_layer_key(row, col, _MOD);
        if (target != KC_NO) {
            register_mods(MOD_BIT(KC_LCTL));  // hold Left-Ctrl
            tap_code16(target);               // tap the resolved key
            unregister_mods(MOD_BIT(KC_LCTL));
        }
        return false;  // we handled it
    }
    return true;  // let QMK handle all other keycodes normally
}

// ——— Keymaps ————————————————————————————————————————
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [_BASE] = LAYOUT(
    KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,
    KC_A,    KC_S,    KC_D,    KC_F,    KC_G,
    KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,
    MO(_MOD), KC_SPC, KC_ENT
  ),

  [_MOD] = LAYOUT(
    MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS,
    MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS,
    MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS, MOD_PASS,
    KC_TRNS,  KC_TRNS,  KC_TRNS
  ),
};
