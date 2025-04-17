def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1
    
    opponent_cooperation_rate = sum(opponent_history) / len(opponent_history)
    
    recent_window = min(5, len(opponent_history))
    recent_opponent_behavior = opponent_history[-recent_window:]
    recent_cooperation_rate = sum(recent_opponent_behavior) / len(recent_opponent_behavior)
    
    tit_for_tat_likelihood = 0
    for i in range(1, len(my_history)):
        if opponent_history[i] == my_history[i-1]:
            tit_for_tat_likelihood += 1
    
    if len(my_history) > 1:
        tit_for_tat_likelihood /= (len(my_history) - 1)
    
    last_move_defect = opponent_history[-1] == 0
    
    betrayal_pattern = False
    if len(opponent_history) >= 3:
        for i in range(len(opponent_history) - 2):
            if opponent_history[i:i+3] == [1, 1, 0] and my_history[i:i+2] == [1, 1]:
                betrayal_pattern = True
    
    consecutive_defections = 0
    for move in reversed(opponent_history):
        if move == 0:
            consecutive_defections += 1
        else:
            break
    
    endgame = False
    if rounds is not None:
        remaining = rounds - len(my_history)
        if remaining <= 3:
            endgame = True
    
    if endgame:
        return 0
    
    if opponent_cooperation_rate > 0.8:
        if len(my_history) % 10 == 0:
            return 0
        return 1
    
    if tit_for_tat_likelihood > 0.8:
        return 1
    
    if recent_cooperation_rate > opponent_cooperation_rate and recent_cooperation_rate > 0.6:
        return 1
    
    if last_move_defect:
        if consecutive_defections > 3:
            return 1
        return 0
    
    if betrayal_pattern:
        return 0
    
    if opponent_history[-1] == 1:
        return 1
    else:
        if len(my_history) % 5 == 0:
            return 1
        return 0