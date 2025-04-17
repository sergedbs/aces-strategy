def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    # Always defect on the very first round.
    if not my_history:
        return 0
    # For the final round (if rounds is known) defect to maximize points.
    if rounds is not None and len(my_history) + 1 == rounds:
        return 0
    # If opponent has cooperated in the last five rounds consecutively, cooperate this round.
    if len(opponent_history) >= 5 and all(move == 1 for move in opponent_history[-5:]):
        return 1
    # Otherwise, defect.
    return 0