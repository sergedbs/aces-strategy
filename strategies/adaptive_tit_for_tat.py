from __future__ import annotations

def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1
    
    if rounds is not None and len(my_history) == rounds - 1:
        return 0
    
    lookback = 5
    recent_moves = opponent_history[-lookback:] if opponent_history else []
    if recent_moves:
        defects = len(recent_moves) - sum(recent_moves)
        if defects / len(recent_moves) > 0.4:
            return 0
    
    if opponent_history[-1] == 0:
        if len(opponent_history) >= 3 and sum(opponent_history[-3:]) >= 2:
            return 1  
        return 0
    return 1
