def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    round_num = len(my_history) + 1

    if rounds is not None and round_num == rounds:
        return 0

    if round_num == 1:
        return 1

    return opponent_history[-1]