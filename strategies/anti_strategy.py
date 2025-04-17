def strategy(my_history: list[int], opponent_history: list[int], rounds: int) -> int:
    round_num = len(my_history)

    if round_num == 0:
        return 1

    if rounds is not None and round_num + 1 == rounds:
        return 0

    total_rounds = round_num
    coop_rate = opponent_history.count(1) / total_rounds if total_rounds > 0 else 1
    def_rate = opponent_history.count(0) / total_rounds if total_rounds > 0 else 0
    recent_opp = opponent_history[-5:]
    recent_me = my_history[-5:]

    def is_all_c(): return def_rate < 0.05
    def is_all_d(): return coop_rate < 0.05
    def is_tit_for_tat(): return all(opponent_history[i] == my_history[i - 1] for i in range(1, round_num))
    def is_grim_trigger(): return 0 in my_history and opponent_history[my_history.index(0):] == [0] * (round_num - my_history.index(0))
    def is_pavlov():
        if round_num < 3: return False
        return all((my_history[i] == opponent_history[i]) == (my_history[i + 1] == my_history[i]) for i in range(round_num - 2))
    def is_tit_for_2_tats():
        if round_num < 3: return False
        def_count = 0
        for i in range(1, round_num):
            if my_history[i - 1] == 0:
                def_count += 1
            if def_count >= 2 and opponent_history[i] == 0:
                return True
        return False
    def is_random_like(): return 0.35 < coop_rate < 0.65
    def is_generous(): return coop_rate > 0.7 and opponent_history[-1] == 1
    def is_spiteful(): return 0 in my_history and 0 in opponent_history[my_history.index(0):] and 1 not in opponent_history[my_history.index(0):]
    def is_copykitten(): return is_tit_for_tat() and opponent_history.count(0) < 3
    def is_probe(): return opponent_history[:3] == [0, 1, 1] and coop_rate > 0.7
    def is_inverse_tft(): return all(opponent_history[i] != my_history[i - 1] for i in range(1, round_num))
    def is_lookback(): return round_num >= 5 and opponent_history[-1] == opponent_history[-5]
    def is_switcher(): return round_num >= 4 and len(set(opponent_history[-4:])) > 1
    def is_trigger_happy(): return round_num > 4 and opponent_history[-3:] == [0, 0, 0]
    def is_cycle_cdd(): return round_num > 3 and opponent_history[-3:] == [1, 0, 0]
    def is_cycle_dcc(): return round_num > 3 and opponent_history[-3:] == [0, 1, 1]
    def is_looker(): return round_num > 5 and opponent_history[-2] == my_history[-3]
    def is_alt_pattern(): return round_num > 5 and all(opponent_history[i] != opponent_history[i - 1] for i in range(1, min(round_num, 6)))
    def is_repeater(): return round_num > 3 and len(set(opponent_history[-3:])) == 1
    def is_noisy_tft(): return round_num >= 5 and sum(abs(opponent_history[i] - my_history[i-1]) for i in range(1, 5)) == 1
    def is_soft_mafia(): return opponent_history[:3] == [1, 1, 0] and coop_rate > 0.5
    def is_alt_abuser(): return round_num >= 6 and opponent_history[-6:] == [1, 0, 1, 0, 1, 0]
    def is_defect_after_10(): return round_num >= 10 and opponent_history[9] == 0
    def is_random_then_grim(): return round_num >= 10 and opponent_history[:5].count(0) >= 2 and all(x == 0 for x in opponent_history[5:])

    if is_all_c(): return 0
    if is_all_d(): return 0
    if is_tit_for_tat() or is_copykitten(): return opponent_history[-1]
    if is_grim_trigger(): return 1 if 0 not in my_history else 0
    if is_pavlov(): return my_history[-1] if my_history[-1] == opponent_history[-1] else 1 - my_history[-1]
    if is_tit_for_2_tats(): return opponent_history[-1] if opponent_history[-2:] != [0, 0] else 0
    if is_generous(): return 0
    if is_spiteful(): return 1
    if is_probe(): return 0
    if is_random_like() or is_switcher(): return 0
    if is_inverse_tft(): return 1
    if is_lookback(): return opponent_history[-1]
    if is_trigger_happy(): return 1
    if is_cycle_cdd(): return 1
    if is_cycle_dcc(): return 0
    if is_looker(): return 1
    if is_alt_pattern(): return 0
    if is_repeater(): return opponent_history[-1]
    if is_noisy_tft(): return opponent_history[-1]
    if is_soft_mafia(): return 0
    if is_alt_abuser(): return 0
    if is_defect_after_10(): return 0
    if is_random_then_grim(): return 0

    if opponent_history[-1] == 0: return 0
    if round_num >= 2 and my_history[-1] == 0 and opponent_history[-2:] == [0, 1]: return 1
    return 1