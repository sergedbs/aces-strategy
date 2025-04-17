def strategy(my_history, opponent_history, rounds):
    if not opponent_history:
        return 1

    total_moves = len(opponent_history)
    coop_rate = sum(opponent_history) / total_moves
    recent = opponent_history[-5:] if total_moves >= 5 else opponent_history
    recent_rate = sum(recent) / len(recent)

    last_move = opponent_history[-1]
    last_two = opponent_history[-2:] if total_moves >= 2 else []
    last_four = opponent_history[-4:] if total_moves >= 4 else []

    if total_moves >= 10 and sum(opponent_history) == 0:
        return 0

    if total_moves >= 10 and sum(opponent_history) == total_moves:
        return 1

    if total_moves >= 3:
        mimic = True
        for i in range(1, total_moves):
            if i < len(my_history) and opponent_history[i] != my_history[i - 1]:
                mimic = False
                break
        if mimic:
            return 1

    if total_moves >= 4 and opponent_history[-4:] == [1, 0, 1, 0]:
        return 0

    if last_two == [0, 0]:
        return 0

    if recent_rate < coop_rate - 0.3:
        return 0

    if coop_rate > 0.8:
        return 1

    if coop_rate < 0.2:
        return 0

    if 0.4 < coop_rate < 0.6:
        return 0 if my_history and my_history[-1] == 1 else 1

    return last_move
