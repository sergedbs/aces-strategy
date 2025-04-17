def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1  # First move: always cooperate

    total_moves = len(opponent_history)
    coop_ratio = opponent_history.count(1) / total_moves
    defect_ratio = opponent_history.count(0) / total_moves

    # Revenge if opponent defected twice in a row
    if total_moves >= 2 and opponent_history[-2:] == [0, 0]:
        return 0

    # Forgiveness if opponent cooperates twice after being punished
    if total_moves >= 2 and my_history[-2:] == [0, 0] and opponent_history[-2:] == [1, 1]:
        return 1

    # Trust opponent if they're mostly cooperative
    if coop_ratio >= 0.7:
        return 1

    # Mirror behavior if opponent is moderately hostile
    if defect_ratio > 0.4:
        return opponent_history[-1]

    # Default to cooperation
    return 1

