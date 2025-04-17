from __future__ import annotations

def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:  
        return 1 
    total_rounds = len(opponent_history)
    opponent_defects = opponent_history.count(0)
    my_defects = my_history.count(0)
    if total_rounds >= 2 and opponent_history[-1] == 0 and opponent_history[-2] == 0:
        return 0  
    if opponent_defects / total_rounds > 0.5:
        return 0  
    if my_defects >= 10 and my_history[-2:].count(0) < 2:
        return 1  
    if rounds is not None and total_rounds == rounds - 1:
        return 0  
    return 1 