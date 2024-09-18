from controller import Controller
from midi.midiwriter import MidiWriter
from seqmorph import (EucMorpher, SimpleProbStepAlg, SimpleProbStepAlgV2,
                      DirectMorph100, DirectMorph50, MegaMorphV1, ProbStep)
from seq import StepSequence
import gui

if __name__ == '__main__':
    app = gui.GUI()
    app.run()
    