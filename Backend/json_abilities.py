from constants import BREAKDOWNS, START_CREDITS, ALL_ABILITIES, ROYALE_ABILITIES

def start_elixir_json(elixir_cap):
    return {
        "values": {
            code: {
                "elixir": BREAKDOWNS[code].elixir,
            }
            for code in ROYALE_ABILITIES
        },
        "elixir_cap": elixir_cap
    }

def start_credit_json(credit_cap):
    return {
        "values": {
            code: {
                "credits": BREAKDOWNS[code].credits,
                "reload": BREAKDOWNS[code].reload,
            }
            for code in ALL_ABILITIES
        },
        "credits": credit_cap,
    }

def start_json(settings):
    if settings["ability_type"] == "credits":
        return start_credit_json(settings["credit_cap"])
    return start_elixir_json(settings["elixir_cap"])

def validate_ability_selection(data, settings):
    if len(data) > settings["deck_size"]:
        return False
    if settings["ability_type"] == "credits":
        total = sum([BREAKDOWNS[code].credits * data[code] for code in data])
        return total <= settings["credit_cap"]
    return True
