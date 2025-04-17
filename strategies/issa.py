def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    defect_streak = 0
    total_defects = 0
    revenge_mode = False
    revenge_timer = 0

    for move in opponent_history:
        if move == 0:
            total_defects += 1
            defect_streak += 1
        else:
            defect_streak = 0

        if defect_streak >= 2 or total_defects >= 5:
            revenge_mode = True
            revenge_timer = 5

    history_length = len(my_history)
    if history_length >= 1 and revenge_mode:
        revenge_timer -= min(history_length, 5)
        if revenge_timer <= 0:
            revenge_mode = False

    if not opponent_history:
        return 1

    if revenge_mode:
        return 0

    opponent_pred = opponent_history[-1]

    if opponent_pred == 1:
        score_if_coop = 3
        score_if_defect = 5
    else:
        score_if_coop = 0
        score_if_defect = 1

    return 1 if score_if_coop > score_if_defect else 0
