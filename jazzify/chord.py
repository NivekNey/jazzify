SCALE = [
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
]


class Chord:
    def __init__(
        self,
        key: str,
        shift: int,
        alt: str,
    ) -> None:
        self.key = key
        self.shift = shift
        self.alt = alt
        self.validate()

    @classmethod
    def from_str(cls, chord_str) -> "Chord":

        raw = chord_str[:]
        shift = 0
        alt = ""

        if not chord_str:
            raise ValueError("Empty chord string")

        # if no # or b exist, first char is key, the rest are alt (special case: /)

        my_key = chord_str[0]
        chord_str = chord_str[1:]
        if not chord_str:
            return cls(my_key, shift, alt)

        if chord_str[0] in ("#", "b"):
            my_key += chord_str[0]
            chord_str = chord_str[1:]
            if not chord_str:
                return cls(my_key, shift, alt)

        # shift

        if chord_str.startswith("/") and chord_str[1] in SCALE:
            second_chord = cls.from_str(chord_str[1:])
            chord_str = chord_str.replace(f"/{second_chord.key}", "/{slash}")
            shift = SCALE.index(second_chord.key) - SCALE.index(my_key)

        return cls(my_key, shift, chord_str)

    def validate(self):
        if self.key not in SCALE:
            raise ValueError(f"Unexpected key {self.key}")
        return self

    def __str__(self):
        slash = SCALE[(SCALE.index(self.key) + self.shift) % len(SCALE)]
        alt = self.alt
        if "{slash}" in alt:
            alt = alt.format(slash=slash)
        return self.key + alt
