from evdev import ecodes, InputDevice, ff, list_devices
import time

# Find first EV_FF capable event device (that we have permissions to use).
for name in list_devices():
    dev = InputDevice(name)
    if ecodes.EV_FF in dev.capabilities():
        break

rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xffff)
effect_type = ff.EffectType(ff_rumble_effect=rumble)
duration_ms = 1000

effect = ff.Effect(
    ecodes.FF_RUMBLE, -1, 0,
    ff.Trigger(0, 0),
    ff.Replay(10000, 0),
    ff.EffectType(ff_rumble_effect=rumble)
)

repeat_count = 1
effect_id = dev.upload_effect(effect)
dev.write(ecodes.EV_FF, effect_id, repeat_count)
time.sleep(duration_ms / 1000)
dev.erase_effect(effect_id)

time.sleep(duration_ms / 1000)

effect_id = dev.upload_effect(effect)
dev.write(ecodes.EV_FF, effect_id, repeat_count)
time.sleep(duration_ms / 1000)
dev.erase_effect(effect_id) 
