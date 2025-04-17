def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1

    punish_cycle = [0, 0, 1]
    punish_index = 0

    last_defect_round = None
    for i in range(len(opponent_history) - 1, -1, -1):
        if opponent_history[i] == 1:
            break
        if opponent_history[i] == 0:
            last_defect_round = i
            break

    if last_defect_round is not None:
        steps_since_defect = len(opponent_history) - 1 - last_defect_round
        cycle_step = steps_since_defect % 3
        return punish_cycle[cycle_step]
    else:
        return 1
