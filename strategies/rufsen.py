def strategy(
    my_history: list[int], opponent_history: list[int], rounds: int | None
) -> int:
    current_round = len(my_history)

    if current_round < 2:
        return 1

    if opponent_history.count(0) >= 3:
        return 0

    if rounds is not None and current_round > 0.8 * rounds:
        return 0

    recent_opponent_moves = opponent_history[-5:]
    if 0 in recent_opponent_moves:
        return 0

    return opponent_history[-1]
