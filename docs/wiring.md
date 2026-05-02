# Wiring Guide

## Schematic (text)

```
                    ┌─────────────┐
                    │    ESP32    │
                    │             │
          GPIO 13 ──┤ BUZZER_PIN  ├──► (+) Passive Buzzer (−) ──► GND
                    │             │
          GPIO 14 ──┤ BUTTON_PIN  ├──► Button leg A
                    │             │         │
              GND ──┤ GND         │    Button leg B ──► 3.3 V
                    │             │         │
                    │             │    10 kΩ pull-down
                    │             │         │
                    └─────────────┘        GND
```

## Component Notes

### Passive Buzzer
A **passive** buzzer requires an external PWM signal to produce sound — it contains no internal oscillator.  
Do **not** use an active buzzer (it produces only a fixed tone regardless of PWM frequency).

### Pull-down Resistor
The 10 kΩ resistor between `BUTTON_PIN` and GND keeps the GPIO at a known LOW state when the button is not pressed.  
When pressed, the button connects the pin to 3.3 V → reads HIGH.

### Pin Variants

| Environment | BUZZER_PIN | BUTTON_PIN |
|-------------|-----------|-----------|
| Wokwi simulator | 13 | 14 |
| Physical DevKit | 27 | 14 |

Change `#define BUZZER_PIN` in `midi_player.ino` accordingly.
