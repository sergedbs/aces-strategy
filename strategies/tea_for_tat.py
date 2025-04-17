def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    round_num = len(my_history)
    
    if round_num == 0:
        return 1  # Cooperate on first move
    
    if rounds is not None and round_num == rounds - 1:
        return 0  # Defect on last move
    
    # Tea break at 17:00 (each 24 rounds) and the round after
    if round_num >= 16 and ((round_num - 16) % 24 == 0 or (round_num - 17) % 24 == 0):
        return 1  # Война войной, а tea break с последующим чаепитием по расписанию
    
    # Tit-for-tat for all other rounds
    return opponent_history[-1]
