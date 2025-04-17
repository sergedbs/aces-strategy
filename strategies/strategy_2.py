def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    """
    Advanced adaptive strategy:
    - Randomized and exploratory opening moves.
    - Analyzes opponent's behavior for consistency, forgiveness, and retaliation.
    - Balances exploitation, retaliation, and cooperation for maximum points.
    """

    # Helper function to detect patterns in opponent's behavior
    def detect_pattern(history: list[int]) -> str:
        if len(history) < 3:
            return "unknown"
        if history[-3:] == [1, 1, 1]:  # Cooperates consistently
            return "cooperator"
        if history[-3:] == [0, 0, 0]:  # Defects consistently
            return "defector"
        if history[-3:] == [1, 0, 1] or history[-3:] == [0, 1, 0]:  # Alternates
            return "alternator"
        return "mixed"


    # Randomized opening moves for unpredictability
    if len(my_history) < 5:
        return [0, 1, 1, 0, 1][len(my_history)]

    # Analyze opponent's behavior
    opponent_pattern = detect_pattern(opponent_history)
    opponent_coop_ratio = opponent_history.count(1) / len(opponent_history)

    # Decision-making based on opponent's pattern
    if opponent_pattern == "cooperator" and opponent_coop_ratio > 0.8:
        return 1  # Exploit cooperators by cooperating
    elif opponent_pattern == "defector" or opponent_coop_ratio < 0.2:
        return 0  # Retaliate against defectors
    elif opponent_pattern == "alternator":
        return 0 if my_history[-1] == 1 else 1  # Try to disrupt alternating strategies
    else:
        # Mixed behavior: use probabilistic defection strategy
        return 1 if sum(my_history[-3:]) < 2 else 0

    # Default fallback (tit-for-tat)
    return opponent_history[-1] if opponent_history else 1