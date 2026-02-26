import random

class SeededRandom:
    def __init__(self, seed):
        self.seed = seed
        self.srand = random.Random(seed)
    
    def randint(self, a, b):
        return self.srand.randint(a, b)
    
    def randchance(self, chance) -> bool:
        return self.srand.randint(0, 100) < chance + 1
    
    def randfloat(self):
        return self.srand.random()