from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from seq import StepSequence


class MidiWriter:
    def __init__(self):
        self._mid = MidiFile()
        self._track = MidiTrack()
        self._mid.tracks.append(self._track)
        self._mid.ticks_per_beat = 480
        self._tempo: int = 120
        self._subdivision: int = 4
        self._timestep = self._mid.ticks_per_beat // self._subdivision
        self._timer = 0

    def add(self, s: StepSequence):
        if not s.tempo() == self._tempo:
            self._tempo = s.tempo()
            self._track.append(MetaMessage(
                'set_tempo', tempo=bpm2tempo(self._tempo)
            ))
        if not s.subdivision() == self._subdivision:
            self._subdivision = s.subdivision()
            self._timestep = self._mid.ticks_per_beat // self._subdivision

        for step in s.sequence():
            if step.onset:
                self._track.append(Message(
                    'note_on', note=s.note(), velocity=step.velocity, time=self._timer))
                self._track.append(Message(
                    'note_off', note=s.note(), time=self._timestep))
                self._timer = 0
            else:
                self._timer += self._timestep

    def save(self, filename: str = 'output.mid'):
        self._track.append(MetaMessage(
            'end_of_track', time=self._timer
        ))
        self._mid.save(filename=filename)

    def print(self):
        for i, track in enumerate(self._mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
                print(msg)
