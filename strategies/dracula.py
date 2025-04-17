def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not my_history:
        return 1

    current_round = len(my_history)

    if current_round <= 50:
        return opponent_history[-1]

    else:
        first_50_cooperation_rate = sum(opponent_history[:50]) / 50

        if first_50_cooperation_rate > 0.7:
            forgiveness_frequency = 5
        elif first_50_cooperation_rate > 0.5:
            forgiveness_frequency = 7
        else:
            forgiveness_frequency = 10

        rounds_after_50 = current_round - 50
        if rounds_after_50 % forgiveness_frequency == 0:
            return 1
        else:
            return opponent_history[-1]
