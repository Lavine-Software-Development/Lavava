def shrink(amount):
    return abs(amount) * -1

def stall(amount):
    return 0


def doubleAttack(contested):
    return 2 if contested else 1

def halfAttack(contested):
    return 0.5 if contested else 1


def freeAttack(contested):
    return 0 if contested else 1


noGrowthFreeAttack = {
    'attackCost': freeAttack,
    'growthMultiplier': stall
}


