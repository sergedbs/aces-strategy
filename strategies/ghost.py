def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 0  

    opp_coop = sum(opponent_history)
    
    if opp_coop > 15:
        return 0
    
    if len(opponent_history) >= 15 and sum(opponent_history[-15:]) == 0:
        return 0
    
    return len(my_history) % 2