from dataclasses import dataclass


@dataclass
class Step:
    onset: bool = False
    velocity: int = 0

    def __str__(self):
        return '| ' + ('x' if self.onset else '.') + ' | '  # + str(self.velocity)


class StepSequence:

    def __init__(self, length: int = 0, note: int = 36, default_velocity: int = 100,
                 tempo: int = 120, subdivision: int = 4):
        self._note = note
        self._default_velocity = default_velocity
        self._tempo = tempo
        self._subdivision = subdivision
        self._sequence = [Step() for _ in range(length)]

    def init_from_list(self, rhythmic_pattern: list):
        self._sequence = [Step() for _ in range(len(rhythmic_pattern))]
        for i, element in enumerate(rhythmic_pattern):
            if element:
                self.set_step(i)
        return self

    def __str__(self):
        s = 'STEP SEQUENCE\n'
        s += ('note: ' + str(self._note) + ', default_velocity: ' + str(self._default_velocity)
              + ', length: ' + str(len(self._sequence)) + '\n')
        seq = []
        for i in range(len(self._sequence)):
            seq.append(str(i) + ':\t' + str(self._sequence[i]))
        return s + '\n'.join(seq)

    def seq_string(self):
        seq = []
        for i in range(len(self._sequence)):
            seq.append(str(i+1) + ':\t' + str(self._sequence[i]))
        return '\n'.join(seq)

    def rhythm_notation(self):
        return '[' + ''.join(['x' if step.onset else '.' for step in self._sequence]) + ']'

    def toggle_step(self, index: int):
        self._sequence[index].onset = not self._sequence[index].onset

    def set_step(self, index: int, velocity: int = None):
        self._sequence[index].onset = True
        self._sequence[index].velocity = velocity if velocity is not None else self._default_velocity

    def add(self, onset: bool = False, velocity: int = None):
        if velocity is None:
            velocity = self._default_velocity
        self._sequence.append(Step(onset, velocity))

    def has_onset(self):
        return any(step.onset for step in self._sequence)

    def is_same_rhythm(self, other):
        if not isinstance(other, StepSequence):
            return False
        if self.length() != other.length():
            return False
        for i in range(self.length()):
            if not self._sequence[i].onset == other.sequence()[i].onset:
                return False
        return True

    def length(self):
        return len(self._sequence)

    def sequence(self):
        return self._sequence

    def note(self):
        return self._note

    def default_velocity(self):
        return self._default_velocity

    def tempo(self):
        return self._tempo

    def set_tempo(self, tempo: int):
        self._tempo = tempo

    def subdivision(self):
        return self._subdivision

    def set_subdivision(self, subdivision: int):
        self._subdivision = subdivision
