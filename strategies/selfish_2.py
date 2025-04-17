def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    turn = len(my_history)
    if turn == 0:
        return 0
    if opponent_history[-1] == 0:
        return 0
    def detect_pattern(history, min_len=2, max_len=5):
        for pattern_len in range(min_len, min(max_len, len(history) // 2) + 1):
            pattern = history[-pattern_len:]
            if history[-2 * pattern_len:-pattern_len] == pattern:
                return pattern
        return None
    pattern = detect_pattern(opponent_history)
    if pattern:
        predicted_move = pattern[turn % len(pattern)]
        if predicted_move == 1:
            return 0
        else:
            return 1 if turn % 6 == 0 else 0
    return 1 if turn % 7 == 0 else 0
