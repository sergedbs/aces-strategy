def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1
    if opponent_history.count(0) > 3:
        return 0
    return opponent_history[-1]
