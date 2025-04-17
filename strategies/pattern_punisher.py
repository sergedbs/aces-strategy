def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1

    opponent_coop_rate = sum(opponent_history) / len(opponent_history)

    recent_window = min(3, len(opponent_history))
    recent_coop_rate = sum(opponent_history[-recent_window:]) / recent_window

    if rounds is not None:
        current_round = len(my_history)
        remaining_rounds = rounds - current_round

        if remaining_rounds <= 3 and opponent_coop_rate < 0.5:
            return 0

    is_alternating = False
    if len(opponent_history) >= 4:
        alternating_pattern = True
        for i in range(len(opponent_history) - 3, len(opponent_history) - 1):
            if opponent_history[i] == opponent_history[i + 1]:
                alternating_pattern = False
                break

        is_alternating = alternating_pattern

    if opponent_coop_rate >= 0.7:
        return 0 if len(my_history) % 10 == 9 else 1

    elif opponent_coop_rate <= 0.3:
        return 1 if len(my_history) % 7 == 0 else 0

    elif is_alternating:
        predicted_next = 1 - opponent_history[-1]
        return 0

    else:
        if opponent_history[-1] == 0:
            if len(my_history) % 4 == 0:
                return 1
            return 0
        else:
            return 1