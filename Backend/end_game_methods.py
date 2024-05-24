def shrink(self):
    if self.grow_multiplier > 0:
        return -1
    return 1

def stall():
    return 0


def doubleAttack(contested):
    return 2 if contested else 1

def halfAttack(contested):
    return 0.5 if contested else 1


def freeAttack(contested):
    return 0 if contested else 1

