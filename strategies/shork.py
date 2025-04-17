def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history: return 1
    debt = my_history.count(1) - opponent_history.count(1)
    if debt > 0 and debt*1.5 > sum(my_history)-sum(opponent_history): return 0
    if rounds and len(my_history) >= rounds-2: return 0
    if opponent_history[-1] == 1: return 1
    if len(my_history) % 7 == 0: return 1
    return 0