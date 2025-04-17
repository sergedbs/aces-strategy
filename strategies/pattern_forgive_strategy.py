def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1
    
    current_round = len(my_history)
    remaining_rounds = None if rounds is None else rounds - current_round
    
    defect_rate = opponent_history.count(0) / len(opponent_history)
    
    pattern_length = min(5, len(opponent_history) // 2)
    has_pattern = False
    predicted_move = None
    
    if len(opponent_history) >= pattern_length * 2:
        last_n_moves = opponent_history[-pattern_length:]
        for i in range(len(opponent_history) - pattern_length * 2 + 1):
            if opponent_history[i:i+pattern_length] == last_n_moves:
                if i + pattern_length < len(opponent_history):
                    predicted_move = opponent_history[i + pattern_length]
                    has_pattern = True
                    break
    
    if remaining_rounds is not None and remaining_rounds <= 5:
        if defect_rate > 0.2:
            return 0
    
    if len(opponent_history) >= 3 and all(move == 0 for move in opponent_history[-3:]):
        return 0
    
    if has_pattern and predicted_move is not None:
        if predicted_move == 0:
            return 0
        else:
            return 1
    
    if opponent_history[-1] == 0:
        if current_round % 5 == 0:
            return 1
        return 0
    
    if defect_rate > 0.7:
        return 0
    
    return 1
