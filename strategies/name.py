def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    round_num = len(my_history)

    if round_num < 3:
        return 1

    if round_num == 5:
        if all(move == 0 for move in opponent_history):
            return 0
        elif all(move == 1 for move in opponent_history):
            return 1

    if opponent_history and opponent_history[-1] == 0:
        return 1

    if round_num % 6 == 0:
        return 0

    return 1
