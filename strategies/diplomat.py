def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1
    if len(my_history) == rounds:
        return 0
    r = len(my_history)

    if len(opponent_history) >= 3 and opponent_history[-3:] == [0, 0, 0]:
        return 0

    total = len(opponent_history)
    betrayal_rate = opponent_history.count(0) / total
    recent = opponent_history[-5:] if total >= 5 else opponent_history
    recent_betrayal = recent.count(0) / len(recent)

    pattern_length = 4
    if total >= pattern_length * 2:
        recent_pattern = opponent_history[-pattern_length:]
        for i in range(total - pattern_length * 2):
            window = opponent_history[i:i+pattern_length]
            if window == recent_pattern:
                if my_history[i+pattern_length] == 1 and opponent_history[i+pattern_length] == 0:
                    return 0

    def my_score():
        score = 0
        for my, op in zip(my_history, opponent_history):
            if my == 1 and op == 1:
                score += 3
            elif my == 0 and op == 1:
                score += 5
            elif my == 1 and op == 0:
                score += 0
            else:
                score += 1
        return score / len(my_history)

    avg_score = my_score()

    if r >= 10 and opponent_history[-10:] == [0] * 10:
        return 0

    if len(my_history) >= 2 and my_history[-2:] == [0, 0] and opponent_history[-2:] == [0, 0]:
        return 1

    if avg_score < 2.0 or (betrayal_rate > 0.6 and recent_betrayal > 0.4):
        return 0

    if betrayal_rate > 0.4 and recent_betrayal <= 0.2:
        return 1

    if opponent_history[-1] == 1:
        return 1
    elif len(opponent_history) >= 2 and opponent_history[-2:] == [1, 0]:
        return 1
    else:
        return 0
