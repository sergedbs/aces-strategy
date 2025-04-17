def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1

    if len(opponent_history) < 5:
        return opponent_history[-1]


    last_10 = opponent_history[-10:]
    opp_coop_rate = sum(last_10) / 10
    defect_streak = 0
    current_streak = 0


    for move in last_10:
        if move == 0:
            current_streak += 1
            defect_streak = max(defect_streak, current_streak)
        else:
            current_streak = 0

    if opp_coop_rate < 0.3 or defect_streak >= 3:
        return 0


    if opp_coop_rate > 0.7:
        return 1


    if len(opponent_history) > 15:
        recent = opponent_history[-15:]

        alternations = sum(1 for i in range(1, 15) if recent[i] != recent[i - 1])
        if alternations > 10:
            return 0 if opponent_history[-1] == 1 else 1
    if len(my_history) > 8 and sum(my_history[-8:]) == 0:
        return 1

    return opponent_history[-1] if (len(my_history) % 4 != 0) else 1