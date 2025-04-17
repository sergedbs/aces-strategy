def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    round_number = len(my_history)

    # Friendly opening
    if round_number < 3:
        return 1

    # Find last round opponent defected
    try:
        last_defect = len(opponent_history) - 1 - opponent_history[::-1].index(0)
    except ValueError:
        last_defect = -1  # never defected

    # Fake forgiveness: delay punishment by 2-3 rounds after opponent's betrayal
    if 0 <= last_defect < round_number - 2 and round_number - last_defect == 3:
        return 0  # delayed revenge
    if 0 <= last_defect < round_number - 3 and round_number - last_defect == 4:
        return 0  # optional second strike

    # Opponent has been cooperating consistently: betray sometimes
    coop_streak = 0
    for move in reversed(opponent_history):
        if move == 1:
            coop_streak += 1
        else:
            break
    if coop_streak >= 4:
        return 0  # punish too much trust

    # If we've been nice for 2 turns and opponent is over 70% cooperation, sneak a defection
    coop_ratio = opponent_history.count(1) / round_number
    if my_history[-2:] == [1, 1] and coop_ratio > 0.7:
        return 0

    return 1