import gui
from midi.midiwriter import MidiWriter
from seqmorph import (EucMorpher, SimpleProbStepAlg, SimpleProbStepAlgV2,
                      DirectMorph100, DirectMorph50, MegaMorphV1, TestingNoRandom, ProbStep)
from seq import StepSequence


class Controller:
    def __init__(self, view):
        self.view: gui.GUI = view
        self.mw: MidiWriter = MidiWriter()
        self._oldEucParams = (-1, -1, -1)
        self._oldSeq = None
        self._pos = 0
        self.morphers = {
            "DirectMorph100": DirectMorph100(),
            "MegaMorphV1": MegaMorphV1(),
            "SimpleProbStepAlg": SimpleProbStepAlg(),
            "SimpleProbStepAlgV2": SimpleProbStepAlgV2(),
            "TestingNoRandom": TestingNoRandom()
        }

    def handle_generate(self):
        k = self.view.onsets.get()
        n = self.view.length.get()
        r = self.view.rotation.get()
        a = self.view.amount.get()
        morpher = self.morphers[self.view.morpher.get()]
        note = self.view.note.get()

        tempo = self.view.tempo.get()
        subdivisions = self.view.subdivisions.get()

        seq = self.view.sequence.get()
        num = self.view.num_bars.get()

        s = StepSequence(tempo=tempo, subdivision=subdivisions, note=note).init_from_list(list(int(x) for x in seq))
        m = EucMorpher(s, k, n, r, a, morpher)

        if self._oldEucParams != (k, n, r) or not s.is_same_rhythm(self._oldSeq):
            self._pos = 0

        start_pos = self._pos

        v = m.generate(num, self._pos)
        self._pos = (self._pos + v.length()) % len(m.prob_steps())

        self.mw.add(v)

        self._oldEucParams = (k, n, r)
        self._oldSeq = s

        if self.view.log_option.get() == "print all":
            print(ProbStep.str_list(m.prob_steps()) + '\n')
            print("GENERATED FROM: " + str(start_pos))
            print("GENERATED TO: " + str(self._pos) + '\n')

        if self.view.log_option.get() == "print rhythm" or self.view.log_option.get() == "print all":
            print('---RESULTING RHYTHM---')
            print(v.seq_string())
            print('\n')

    def handle_save(self, filename):
        if self.view.log_option.get() == "print all":
            self.mw.print()
        self.mw.save(filename)
        self.mw = MidiWriter()

    def handle_clear(self):
        self.mw = MidiWriter()
