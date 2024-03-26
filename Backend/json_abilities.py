from constants import BREAKDOWNS, START_CREDITS, ALL_ABILITIES


def start_json():
    return {
        "values": {
            code: {
                "credits": BREAKDOWNS[code].credits,
                "reload": BREAKDOWNS[code].reload,
            }
            for code in ALL_ABILITIES
        },
        "credits": START_CREDITS,
    }


def validate_ability_selection(data):
    total = sum([BREAKDOWNS[code].credits * data[code] for code in data])
    return total <= START_CREDITS
