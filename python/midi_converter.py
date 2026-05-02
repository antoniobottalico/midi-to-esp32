# =============================================================================
# midi_converter.py  (run as Google Colab notebook)
# MIDI-to-ESP32 Converter
#
# Reads a MIDI file, extracts a melody track, applies intelligent
# monophony reduction, and outputs ready-to-paste Arduino C++ code.
# =============================================================================

# ── Dependencies ─────────────────────────────────────────────────────────────
!pip install pretty_midi --quiet

import pretty_midi
from google.colab import files

# =============================================================================
# 1. UPLOAD MIDI FILE
# =============================================================================
print("Upload a MIDI file:")
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
midi = pretty_midi.PrettyMIDI(file_name)

print(f"\nLoaded: {file_name}")
print(f"Duration: {midi.get_end_time():.2f} s")
print(f"Tempo: {midi.estimate_tempo():.1f} BPM  (estimated)")

# =============================================================================
# 2. TRACK OVERVIEW
# =============================================================================
print("\n=== AVAILABLE TRACKS ===")

for i, inst in enumerate(midi.instruments):
    note_count = len(inst.notes)
    kind = "Drums" if inst.is_drum else "Melodic"
    print(f"\n  [{i}] {inst.name or '(unnamed)'}  |  {kind}  |  {note_count} notes")

    # Preview first 5 notes
    for n in inst.notes[:5]:
        freq  = round(pretty_midi.note_number_to_hz(n.pitch))
        dur   = round(n.end - n.start, 3)
        name  = pretty_midi.note_number_to_name(n.pitch)
        print(f"       {name:4s}  {freq:5d} Hz   {dur:.3f} s")

# =============================================================================
# 3. TRACK SELECTION
# =============================================================================
track_index = int(input("\nChoose track number: "))
inst = midi.instruments[track_index]
print(f"Selected: '{inst.name or '(unnamed)'}' — {len(inst.notes)} notes")

# =============================================================================
# 4. RAW NOTE EXTRACTION
# =============================================================================
notes_raw = []

for note in inst.notes:
    freq = pretty_midi.note_number_to_hz(note.pitch)
    notes_raw.append({
        "start": note.start,
        "end":   note.end,
        "freq":  round(freq),
        "name":  pretty_midi.note_number_to_name(note.pitch),
    })

# =============================================================================
# 5. INTELLIGENT MONOPHONY REDUCTION
#    When multiple notes share the same onset time, keep the highest pitch
#    (melodic lead). This simulates what a single buzzer can reproduce.
# =============================================================================
monophony = {}

for n in notes_raw:
    t = round(n["start"], 2)
    if t not in monophony or n["freq"] > monophony[t]["freq"]:
        monophony[t] = n

# =============================================================================
# 6. SORT & STATISTICS
# =============================================================================
notes_final = sorted(monophony.values(), key=lambda x: x["start"])

freqs    = [n["freq"] for n in notes_final]
durations = [(n["end"] - n["start"]) * 1000 for n in notes_final]

print(f"\n=== CONVERSION SUMMARY ===")
print(f"  Raw notes    : {len(notes_raw)}")
print(f"  After mono   : {len(notes_final)}")
print(f"  Freq range   : {min(freqs)} – {max(freqs)} Hz")
print(f"  Duration range: {min(durations):.0f} – {max(durations):.0f} ms")
print(f"  Total time   : {notes_final[-1]['end']:.2f} s")

# =============================================================================
# 7. CODE GENERATION
#    Outputs valid Arduino C++ calls, including inter-note silences (delay).
# =============================================================================
print("\n=== GENERATED CODE FOR ESP32 ===\n")
print("// ── paste inside playMusic() ──────────────────────────────────────")

prev_end = 0.0

for n in notes_final:
    start = n["start"]
    end   = n["end"]

    # Silence gap before this note
    gap = start - prev_end
    if gap > 0.005:                        # ignore gaps < 5 ms (quantisation noise)
        gap_ms = int(gap * 1000)
        print(f"delay({gap_ms});")

    dur_ms = int((end - start) * 1000)
    print(f"playNote({n['freq']}, {dur_ms});   // {n['name']}")

    prev_end = end

print("// ── end of sequence ───────────────────────────────────────────────")
print(f"\n// Total notes: {len(notes_final)}")
