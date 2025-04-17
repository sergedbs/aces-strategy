def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    round_number = len(my_history)

    if round_number < 3:
        return 1
    coop_rate = opponent_history.count(1) / round_number

    fake_random = (sum(my_history) + sum(opponent_history) + round_number) % 10
    if coop_rate > 0.7:
        return 0 if fake_random < 7 else 1
    if coop_rate < 0.4:
        return 0
    return 0 if fake_random < 6 else 1
