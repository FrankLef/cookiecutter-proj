import winsound

scale: int = 440
ratio: float = 1.05946
notes: dict[str, int] = {
    "C": -9,
    "C#": -8,
    "D": -7,
    "D#": -6,
    "E": -5,
    "F": -4,
    "F#": -3,
    "G": -2,
    "G#": -1,
    "A": 0,
    "A#": 1,
    "B": 2,
}

tempered_notes = {}

for note in notes:
    freq: float = scale * ratio ** notes.get(note)  # type: ignore
    tempered_notes[note] = int(freq)


def play_note(note, duration=500):
    winsound.Beep(tempered_notes.get(note), duration)


song = "E E F G G F E D C C D E E D D"
for note in song.split():
    play_note(note)
