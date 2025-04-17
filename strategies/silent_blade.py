def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    # round 1: defect
    if not opponent_history:
        return 1

    # analyze last 5 moves of opponent
    recent = opponent_history[-5:]
    coop_count = recent.count(0)
    defect_count = recent.count(1)

    if coop_count >= 4:
        # exploit if opponent is too nice
        return 1
    elif defect_count >= 3:
        # retaliate if opponent is aggressive
        return 1
    else:
        # mirror last move otherwise
        return opponent_history[-1]