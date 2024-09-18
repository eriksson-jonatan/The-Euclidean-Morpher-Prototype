import copy

from seq import euc
from seq import StepSequence
from .probsteps import ProbStepAlg
from random import random


class EucMorpher:
    def __init__(self, s: StepSequence, onsets, subdivisions, rotation, randomness, algorithm: ProbStepAlg):
        self._algorithm = algorithm
        self._s = copy.deepcopy(s)
        self._e = (StepSequence(note=s.note(), default_velocity=s.default_velocity(),
                                tempo=s.tempo(), subdivision=s.subdivision())
                   .init_from_list(euc(onsets, subdivisions, rotation)))
        self._prob_steps = algorithm.generate_prob_steps(self._s, self._e, randomness)

    def prob_steps(self):
        return self._prob_steps

    def generate(self, num_bars: int = None, start_pos: int = 0) -> StepSequence:
        if num_bars is None or num_bars <= 0:
            length = len(self._prob_steps)
        else:
            length = self._s.length() * num_bars

        v = StepSequence(length=length, note=self._s.note(), default_velocity=self._s.default_velocity(),
                         tempo=self._s.tempo(), subdivision=self._s.subdivision())
        for i in range(v.length()):
            p = self._prob_steps[(i+start_pos) % len(self._prob_steps)].probability
            if random() < p:
                v.set_step(i)
        return v
