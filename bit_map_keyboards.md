enum custom_keycodes {
    LAYER_2_3 = SAFE_RANGE,
};

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case LAYER_2_3:
            if (record->event.pressed) {
                layer_on(2);  // base layer
                layer_on(3);  // overlay on top
            } else {
                layer_off(3);
                layer_off(2);
            }
            return false;
    }
    return true;
}
