def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1


    cooperation_rate = sum(opponent_history) / len(opponent_history)

    recent_window = min(5, len(opponent_history))
    recent_cooperation = sum(opponent_history[-recent_window:]) / recent_window if recent_window > 0 else 0

    end_game = rounds is not None and len(my_history) >= rounds - 5

    if cooperation_rate > 0.8:
        if len(my_history) % 3 == 0:
            return 0

    if 0.5 <= cooperation_rate <= 0.8:
        if opponent_history[-1] == 1:
            if recent_cooperation > 0.6:
                return 0

        elif opponent_history[-1] == 0:
            if cooperation_rate > 0.65 and len(my_history) % 2 == 0:
                return 1
            return 0

    if cooperation_rate < 0.5:
        if recent_cooperation > 0.6 and opponent_history[-1] == 1:
            return 1
        return 0

    if len(opponent_history) >= 4:
        if opponent_history[-2:] == [0, 1] and opponent_history[-4:-2] == [0, 1]:
            return 0

        if len(my_history) >= 3:
            matches = sum(1 for i in range(len(my_history) - 3, len(my_history))
                          if opponent_history[i] == my_history[i - 1])
            if matches >= 3:
                return 1

    if end_game:
        return 0

    if len(my_history) % 5 < 2:
        return 1
    return 0
