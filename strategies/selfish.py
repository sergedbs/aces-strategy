def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not my_history:
        return 0
    
    current_round = len(my_history)
    
    if rounds is not None and current_round >= rounds - 3:
        return 0
    
    opponent_coop_count = sum(opponent_history)
    opponent_coop_rate = opponent_coop_count / len(opponent_history) if opponent_history else 0
    
    if len(opponent_history) >= 3 and all(move == 0 for move in opponent_history[-3:]):
        return 0
    
    is_tit_for_tat = True
    if len(my_history) >= 4:
        for i in range(1, min(5, len(my_history))):
            if opponent_history[i] != my_history[i-1]:
                is_tit_for_tat = False
                break
    
    if is_tit_for_tat and len(my_history) >= 4:
        if my_history[-1] == 1:
            return 0
        else: 
            return 1 
    
    if opponent_coop_rate > 0.8 and len(opponent_history) >= 5:
        return 0
    
    if len(opponent_history) >= 6:
        if opponent_history[-6:] == [0, 1, 0, 1, 0, 1] or opponent_history[-6:] == [1, 0, 1, 0, 1, 0]:
            return 0
        
        if opponent_history[-6:] == opponent_history[-3:] + opponent_history[-3:]:
            next_predicted = opponent_history[-3]  
            return 0 if next_predicted == 1 else 0  
    
    if len(opponent_history) >= 2:
        if opponent_history[-1] == 0 and opponent_history[-2] == 0:
            return 0
        
        if opponent_history[-1] == 0 and my_history[-1] == 1:
            return 0
    
    recent_opponent_coop_rate = sum(opponent_history[-5:]) / 5 if len(opponent_history) >= 5 else opponent_coop_rate
    
    if recent_opponent_coop_rate > 0.6:
        if current_round % 3 != 0:
            return 1
    
    if current_round % 4 == 0 or current_round % 5 == 0:
        return 1
    return 0 
