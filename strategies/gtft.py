def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    current_round = len(my_history)

    if current_round == 0:
        return 1

    last_opponent_move = opponent_history[-1]

    if last_opponent_move == 1:
        return 1

    if current_round % 4 == 0:
        return 1
    else:
        return 0
