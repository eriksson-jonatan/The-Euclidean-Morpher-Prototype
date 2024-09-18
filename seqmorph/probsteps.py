from dataclasses import dataclass, field
from abc import abstractmethod, ABC

import numpy as np
from seq.stepseq import StepSequence


@dataclass
class ProbStep:
    onset: bool = False
    probability: float = 0.00
    properties: set = field(default_factory=set)

    def __str__(self):
        return ('| ' + ('x' if self.onset else '.') + ' | ' + f'{self.probability:.2f}' + '\t| '
                + (str(self.properties) if not len(self.properties) == 0 else ''))

    @staticmethod
    def str_list(data: []) -> str:
        s = 'PROBABILITY STEPS' + '\n' + 'length: ' + str(len(data)) + '\n'
        seq = []
        for i in range(len(data)):
            seq.append(str(i+1) + ':\t' + str(data[i]))
        return s + '\n'.join(seq)


class ProbStepAlg(ABC):
    @abstractmethod
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        pass


class SimpleProbStepAlg(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        seqs = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in seqs])
        prob_steps = []

        # Adds and marks the probability steps that correspond to an onset from the inputted sequences
        for i in range(length):
            if any(seq[i % len(seq)].onset for seq in seqs):
                prob_steps.append(ProbStep(onset=True))
            else:
                prob_steps.append(ProbStep())

        # Calculates appropriate probabilities
        for i in range(length):
            if not prob_steps[i].onset:
                if prob_steps[i-1].onset or prob_steps[(i+1) % length].onset:
                    prob_steps[i].probability = rp/2
            else:
                prob_steps[i].probability = 1 - rp/2

        return prob_steps


class SimpleProbStepAlgV2(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        data = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in data])
        prob_steps = []

        # Adds and marks the probability steps that correspond to an onset from the inputted sequences
        for i in range(length):
            prob_steps.append(ProbStep())
            for seq in data:
                if seq[i % len(seq)].onset:
                    prob_steps[i].onset = True
                    if seq is s.sequence():
                        prob_steps[i].properties.add('base')
                    if seq is e.sequence():
                        prob_steps[i].properties.add('extra')

        for i in range(length):
            if not prob_steps[i].onset:
                adj = (prob_steps[i-1], prob_steps[(i+1) % length])
                if any(step.onset for step in adj):
                    if any('base' in step.properties for step in adj):
                        prob_steps[i].probability = rp/4
                    else:
                        prob_steps[i].probability = rp/2
            else:
                if 'base' in prob_steps[i].properties:
                    prob_steps[i].probability = 1 - rp/4
                else:
                    prob_steps[i].probability = 1 - rp/2

        return prob_steps


class MegaMorphV1(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        data = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in data])
        prob_steps = []

        # Adds and marks the probability steps that correspond to an onset from the inputted sequences
        for i in range(length):
            prob_steps.append(ProbStep())
            for seq in data:
                if seq[i % len(seq)].onset:
                    prob_steps[i].onset = True
                    if seq is s.sequence():
                        prob_steps[i].properties.add('s')
                    if seq is e.sequence():
                        prob_steps[i].properties.add('e')

        for i in range(length):
            adj = (prob_steps[i - 1], prob_steps[(i + 1) % length])
            if not prob_steps[i].onset:
                if any('s' in step.properties and 'e' in step.properties for step in adj):
                    prob_steps[i].probability = rp/4
                elif any('s' in step.properties for step in adj):
                    prob_steps[i].probability = rp/2
            else:
                if 's' in prob_steps[i].properties and 'e' in prob_steps[i].properties:
                    prob_steps[i].probability = 1 - rp/4
                elif 's' in prob_steps[i].properties:
                    prob_steps[i].probability = 1 - rp/2
                elif 'e' in prob_steps[i].properties:
                    prob_steps[i].probability = rp

        return prob_steps


class DirectMorph100(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        data = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in data])
        prob_steps = []

        # Adds and marks the probability steps that correspond to an onset from the inputted sequences
        for i in range(length):
            prob_steps.append(ProbStep())
            for seq in data:
                if seq[i % len(seq)].onset:
                    prob_steps[i].onset = True
                    if seq is s.sequence():
                        prob_steps[i].properties.add('s')
                    if seq is e.sequence():
                        prob_steps[i].properties.add('e')

        # Assigns probabilities to the probability steps
        for i in range(length):
            if prob_steps[i].onset:
                if 's' in prob_steps[i].properties and 'e' in prob_steps[i].properties:
                    prob_steps[i].probability = max(1-rp, rp)
                elif 's' in prob_steps[i].properties:
                    prob_steps[i].probability = 1 - rp
                elif 'e' in prob_steps[i].properties:
                    prob_steps[i].probability = rp

        return prob_steps


class DirectMorph50(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        data = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in data])
        prob_steps = []

        # Adds and marks the probability steps that correspond to an onset from the inputted sequences
        for i in range(length):
            prob_steps.append(ProbStep())
            for seq in data:
                if seq[i % len(seq)].onset:
                    prob_steps[i].onset = True
                    if seq is s.sequence():
                        prob_steps[i].properties.add('s')
                    if seq is e.sequence():
                        prob_steps[i].properties.add('e')

        for i in range(length):
            if prob_steps[i].onset:
                if 's' in prob_steps[i].properties:
                    prob_steps[i].probability = 1 - (rp/2)
                elif 'e' in prob_steps[i].properties:
                    prob_steps[i].probability = rp/2

        return prob_steps


class TestingNoRandom(ProbStepAlg):
    def generate_prob_steps(self, s: StepSequence, e: StepSequence, r: int) -> list[ProbStep]:
        rp = np.clip(r/100, 0, 1)
        data = [seq.sequence() for seq in (s, e) if seq.has_onset()]
        length = np.lcm.reduce([len(item) for item in data])
        prob_steps = []

        for i in range(length):
            prob_steps.append(ProbStep())
            for seq in data:
                if seq[i % len(seq)].onset:
                    prob_steps[i].onset = True
                    prob_steps[i].probability = 1.00
                    if seq is s.sequence():
                        prob_steps[i].properties.add('s')
                    if seq is e.sequence():
                        prob_steps[i].properties.add('e')

        return prob_steps
