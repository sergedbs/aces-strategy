from __future__ import annotations

def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1

    if len(opponent_history) < 20:
        if len(opponent_history) >= 2 and opponent_history[-1] == 0 and opponent_history[-2] == 0:
            return 0
        else:
            return 1

    def detect_always_cooperate(history):
        return all(move == 1 for move in history)

    def detect_always_defect(history):
        return all(move == 0 for move in history)

    def detect_tit_for_tat(history, my_history):
        if len(history) < 2:
            return False
        return all(history[i] == my_history[i - 1] for i in range(1, len(history)))

    def detect_alternating(history):
        if len(history) < 2:
            return False
        return all(history[i] != history[i + 1] for i in range(len(history) - 1))

    def detect_grim_trigger(opp_history, my_hist):
        for i in range(len(my_hist)):
            if my_hist[i] == 0 and all(m == 0 for m in opp_history[i:]):
                return True
        return False

    initial_opponent = opponent_history[:20]
    initial_my = my_history[:20]

    if detect_grim_trigger(opponent_history, my_history):
        return 0

    if detect_always_cooperate(initial_opponent):
        return 1

    elif detect_always_defect(initial_opponent):
        return 0

    elif detect_tit_for_tat(initial_opponent, initial_my):
        return opponent_history[-1]

    elif detect_alternating(initial_opponent):
        return 1 - opponent_history[-1]

    else:
        coop_rate = initial_opponent.count(1) / 20
        if coop_rate <= 0.5:
            return 0
        else:
            return opponent_history[-1]