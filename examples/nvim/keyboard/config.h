
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
#define LAYER_STATE_16BIT

#define RGB_MATRIX_STARTUP_SPD 60
