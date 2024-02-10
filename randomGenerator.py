import random


class RandomGenerator:
    def __init__(self, seed):
        self.seed = seed
        self.random = random.Random(seed)

    def randint(self, start, stop):
        rand_int = self.random.randint(start, stop)
        self.update_seed()
        return rand_int

    def update_seed(self):
        self.seed = int(self.seed * 1.1) % (2**32)
        self.random.seed(self.seed)
