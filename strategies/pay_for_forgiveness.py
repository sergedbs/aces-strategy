
def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    current_round = len(my_history)
    if current_round == 0:
        return 1

    cycle_position = current_round % 10
    if cycle_position == 0:
        cycle_position = 10

    recent_window = opponent_history[-cycle_position:]
    betrayals = recent_window.count(0)

    if betrayals >= 2:
        return 0
    return 1
