
#include QMK_KEYBOARD_H
#include "eeprom.h"
extern rgb_config_t rgb_matrix_config;

enum keycodes = {
	keycodes=SAFE_RAN
};
enum layers = {
	_syms,
	_nums,
	_delete,
	_mouse,
	_fn,
	_base
};
const uint16_t PROGMEM keymap[][4][12] = {
[_base] = {qwertdelbacyuiopasdfg'enterhjkl;zxcvbesctabnm,./ctlaltfnsftsymsspacenonumsmousenoosalt,
	[_syms] = {nononononotranstransno!{}@nonononono`transno#()$nononononotranstransno|[]&transtranstranstranstranstranstranstranstranstranstranstrans,
	[_nums] = {0123notranstransno%~\no.456no`transno-+/*=789nocalctransnono<>^transtranstranstranstranstranstranstranstranstranstranstrans,
	[_delete] = {nononononotranstransnononononod_linetabd_worddelnonotransnobacb_wordenterb_linenononononotranstransnononononotranstranstranstranstranstranstranstranstranstranstranstrans,
	[_mouse] = {nor_clkm_upl_clknotranstransnoenterupnononom_leftm_downm_rightnonotransw_leftleftdownrightw_rightp_leftp_upnop_downp_righttranstransnohomenoendnotranstranstranstranstranstranstranstranstranstranstranstrans,
	[_fn] = {f1f2f3f4f5f6f7f8f9f10f11f12nonononononobrt-brt+vol-vol+novol_mnononononononononononopausetranstranstranstranstranstransnotranstranstranstranstrans
};
const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT][3] = {

};
uint8_t layer_state_set_user(uint8_t state){
	state = update_tri_layer_state(state, _syms, _nums, _delete);
	return state
};

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
