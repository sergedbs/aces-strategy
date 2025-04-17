def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    defection_count = 0
    total = hash(str(my_history[-20:]) + str(opponent_history[-20:]))  # Consider the last 20 moves for randomness
    
    # Have a one in 17 chance to defect (snap)
    if hash(total * 663937) % 17 == 0:
        return 0  # Defect
    
    # Check the opponent's recent defections
    for i in range(len(opponent_history)):
        if opponent_history[i] == 0:  # If the opponent defected
            defection_count += 1
        else:
            defection_count = 0  # Reset if the opponent cooperated
    
    # If the opponent defected in the past few rounds, act based on a pseudo-random decision
    if defection_count >= 1:
        # Make a pseudo-random decision based on the total history using a mathematical approach
        total = hash(str(my_history[-5:]) + str(opponent_history[-5:]))  # Take the last 5 rounds for calculation
        if (total % 3) == 0:  # 1 in 3 chance to defect
            return 0  # Defect
        else:
            return 1  # Cooperate

    # Default strategy when no recent defections by the opponent
    return 1  # Cooperate if the opponent has been cooperative