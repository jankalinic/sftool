AVERAGE_EXP_PER_SEGMENT=10000

def get_best_quest(quest1, quest2, quest3):
    quest_values = {
        quest1: get_quest_value(quest1),
        quest2: get_quest_value(quest2),
        quest3: get_quest_value(quest3)
    }
    best_value = max(quest_values[quest1], quest_values[quest2], quest_values[quest3])
    return list(quest_values.values()).index(best_value)


def get_quest_value(quest):
    segment = quest["energy_cost"] / 2.5
    value = quest["exp"] + (4 - segment) * AVERAGE_EXP_PER_SEGMENT
    return value