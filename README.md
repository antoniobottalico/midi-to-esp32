# 🎵 MIDI to ESP32 Player

A full embedded audio pipeline that converts MIDI files into real-time sound on an ESP32 using PWM synthesis on a passive buzzer.

---

## ⚙️ System Overview

```
MIDI file → Python parser → C++ code generation → ESP32 firmware → 🔊 audio output
```

---

## 🚀 Features

- MIDI file parsing using Python (`pretty_midi`)
- Monophonic melody extraction (lead note selection — highest pitch priority)
- Accurate timing conversion: MIDI timestamps → millisecond delays
- ESP32 PWM audio synthesis via LEDC peripheral
- Button-triggered playback with configurable countdown
- Serial debug output for every note and system event

---

## 🔌 Hardware

| Component | Details |
|-----------|---------|
| ESP32 | Any DevKit (WROOM, S3, …) |
| Passive buzzer | 3–5 V, PWM-driven |
| Push button | Normally open, tactile |
| Resistor | 10 kΩ pull-down |

### Wiring

```
ESP32 GPIO 13 ──► Buzzer (+) | Buzzer (−) ──► GND
ESP32 GPIO 14 ──► Button ──► 3.3 V
10 kΩ between GPIO 14 and GND (pull-down)
```

> 💡 Change `BUZZER_PIN` to `27` when using physical hardware instead of the Wokwi simulator.

---

## 📊 Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  MIDI File  │────►│ Python Converter  │────►│  C++ code block │
└─────────────┘     │  (Google Colab)  │     │  playNote(...)  │
                    └──────────────────┘     └────────┬────────┘
                                                      │ paste
                                             ┌────────▼────────┐
                                             │  ESP32 Firmware  │
                                             │  midi_player.ino │
                                             └────────┬────────┘
                                                      │ PWM
                                             ┌────────▼────────┐
                                             │  Passive Buzzer  │
                                             │   🔊 audio out   │
                                             └─────────────────┘
```

---

## 🎯 Key Technical Ideas

**Monophony reduction** — MIDI tracks often contain chords. Since a single buzzer produces one frequency at a time, overlapping notes are resolved by keeping the highest pitch (melodic lead) at each onset:

```python
if t not in monophony or n["freq"] > monophony[t]["freq"]:
    monophony[t] = n
```

**Note duration model** — each note is split into two phases to create a perceivable gap between consecutive same-pitch notes:

```
|←──── NOTE_ON 90% ────►|← NOTE_OFF 10% →|
      buzzer active          buzzer silent
```

**PWM synthesis** — no DAC or audio codec. The ESP32 LEDC peripheral drives a square wave at the target frequency directly into the buzzer, similar to how classic 8-bit computers produced sound.

---

## 🛠️ How to Use

### Step 1 — Convert your MIDI (Google Colab)

1. Open `python/midi_converter.py` in [Google Colab](https://colab.research.google.com)
2. Run all cells and upload your `.mid` file
3. Select the track you want (melody, lead, etc.)
4. Copy the printed `playNote(...)` output

### Step 2 — Flash the ESP32 (Arduino IDE)

1. Open `esp32/midi_player.ino`
2. Paste the copied code inside `playMusic()`
3. Select board: **ESP32 Dev Module**
4. Upload

### Step 3 — Play

Press the button → wait 2 seconds → melody plays.

---

## ⚙️ Configuration

All parameters are defined at the top of `midi_player.ino`:

```cpp
#define BUTTON_PIN      14    // GPIO for the button
#define BUZZER_PIN      13    // GPIO for the buzzer (use 27 on real HW)
#define NOTE_ON_RATIO  0.9f   // fraction of note duration spent playing
#define NOTE_OFF_RATIO 0.1f   // fraction used as inter-note silence
#define START_DELAY_MS 2000   // ms between button press and playback start
```

---

## 📦 Structure

```
midi-to-esp32/
├── esp32/
│   └── midi_player.ino      # Arduino sketch
├── python/
│   └── midi_converter.py    # Google Colab MIDI converter
├── docs/
│   └── wiring.md            # Wiring details
└── README.md
```

---

## 📹 Demo

🎮 **Song:** Tetris Theme (Korobeiniki)

▶️ [Watch demo video — TetrisBottalicoESP32](https://drive.google.com/file/d/17fskx3cny0j60wiSCdU6wFZZDLuz0si2/view?usp=sharing)

🔗 [Live simulation on Wokwi](https://wokwi.com/projects/462350508748068865)

---

## 🔭 Future Ideas

- Polyphonic playback with two buzzers (dual PWM channels)
- SD card support — load MIDI at runtime, no reflashing needed
- OLED display showing current note and progress
- BLE / Wi-Fi remote trigger

---

## 👤 Author

**Antonio Bottalico** — [GitHub](https://github.com/AntonioBottalico)

---

## 📜 License

MIT — Copyright (c) 2026 Antonio Bottalico
