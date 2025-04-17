def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    def ema(history: list[int], alpha_value: float) -> float:
        if not history:
            return 1.0
        ema_value = history[0]
        for movement in history[1:]:
            ema_value = alpha_value * movement + (1 - alpha_value) * ema_value
        return ema_value

    def sigmoid(x: float, k: float = 10) -> float:
        return 1.0 / (1.0 + 2.71828 ** (-k * x))

    def pseudo_random(seed: int) -> float:
        return ((seed * 16807) % 2147483647) / 2147483647.0

    def detect_pattern(history: list[int], max_length: int = 4) -> list[int] | None:
        if len(history) < 2 * max_length:
            return None

        if len(set(history[-max_length:])) == 1:
            return None

        for pattern_length in range(2, max_length + 1):
            recent = history[-pattern_length:]
            previous = history[-2 * pattern_length:-pattern_length]
            if recent == previous:
                return recent
            
        return None

    def detect_cycle(history: list[int], max_cycle: int = 5) -> list[int] | None:
        if len(history) < 3 * max_cycle:
            return None

        recent_variance = len(set(history[-max_cycle * 2:]))
        if recent_variance <= 1:
            return None

        for cycle_length in range(2, max_cycle + 1):
            is_cycle = True
            for offset in range(cycle_length):

                values = [history[-(i * cycle_length + offset)] for i in range(1, 4)
                          if -(i * cycle_length + offset) >= -len(history)]
                if len(values) < 3 or not all(v == values[0] for v in values):
                    is_cycle = False
                    break
            if is_cycle:
                return history[-cycle_length:]
        return None

    def ngram_analysis(history: list[int], ng: int = 3) -> tuple[int | None, float]:
        if len(history) < ng + 1:
            return None, 0.0

        last_ngram = tuple(history[-ng:])
        next_moves = {}

        for j in range(len(history) - ng):
            current_ngram = tuple(history[j:j + ng])
            if current_ngram == last_ngram and j + ng < len(history):
                following_move = history[j + ng]
                next_moves[following_move] = next_moves.get(following_move, 0) + 1

        if next_moves:
            predicted_movement = max(next_moves, key=next_moves.get)
            confidence = next_moves[predicted_movement] / sum(next_moves.values())
            return predicted_movement, confidence
        return None, 0.0


    n = len(my_history)
    if n < 5:
        if n == 0:
            return 1
        if n == 1:
            return 1 if opponent_history[0] == 1 else 0
        if opponent_history[-1] == 0 and opponent_history[-2:].count(0) == 2:
            return 0
        return 1

    if rounds is not None:
        rounds_remaining = rounds - n
        if rounds_remaining <= 1:
            return 0
        elif rounds_remaining <= 3:
            if n >= 10 and sum(opponent_history[-10:]) / 10 > 0.8 and opponent_history[-3:].count(1) >= 2:
                if rounds_remaining == 2:
                    return 1
            return 0

    my_score = 0
    opp_score = 0
    if n >= 10 and (n % 5 == 0 or n <= 15):
        for i in range(n):
            if my_history[i] == 1 and opponent_history[i] == 1:
                my_score += 3
                opp_score += 3
            elif my_history[i] == 1 and opponent_history[i] == 0:
                my_score += 0
                opp_score += 5
            elif my_history[i] == 0 and opponent_history[i] == 1:
                my_score += 5
                opp_score += 0
            else:
                my_score += 1
                opp_score += 1

    score_difference = my_score - opp_score

    betrayal_memory = 0
    recent_betrayal = False

    for i in range(max(1, n - 10), n):
        if i > 0 and my_history[i - 1:i + 1] == [1, 1] and opponent_history[i - 1:i + 1] == [0, 0]:
            betrayal_memory += 1
            recent_betrayal = True

    if betrayal_memory > 0 and n > 20:
        betrayal_memory = max(0, betrayal_memory - (n // 30))

    window_size = min(10, n)
    recent_window = opponent_history[-window_size:] if window_size > 0 else []
    weighted_defections = 0

    if n >= 5:
        weighted_defections = sum((0.8 ** i) * (1 - opponent_history[-(i + 1)])
                for i in range(min(10, n)))
        
    pattern = None
    cycle_pattern = None
    predicted_defection = False
    pattern_confidence = 0.0

    if n > 10 and n % 4 == 0:
        pattern = detect_pattern(opponent_history)

        if n % 12 == 0 and n > 15:
            cycle_pattern = detect_cycle(opponent_history)
            if cycle_pattern and not pattern:
                pattern = cycle_pattern
                predicted_move = pattern[n % len(pattern)]
                predicted_defection = (predicted_move == 0)
                pattern_confidence = 0.65

        if n % 6 == 0 or pattern is None:
            ngram_move, ngram_confidence = ngram_analysis(opponent_history, 3)
            if ngram_move is not None and ngram_confidence > 0.65:
                predicted_defection = (ngram_move == 0)
                pattern_confidence = ngram_confidence

        if pattern and not cycle_pattern:
            predicted_move = pattern[0]
            predicted_defection = (predicted_move == 0)
            pattern_confidence = 0.7

    recent_coop = ema(recent_window, 0.3) if recent_window else 0.5
    overall_coop = sum(opponent_history) / n if n > 0 else 1.0
    combined_coop = 0.6 * recent_coop + 0.4 * overall_coop

    var_recent = 0.0
    if n >= 5 and (n % 5 == 0 or n <= 15):
        mean = sum(recent_window) / len(recent_window)
        var_recent = sum((x - mean) ** 2 for x in recent_window) / len(recent_window)

    opponent_type = "unknown"
    if n >= 10:
        defection_rate = 1 - overall_coop

        if defection_rate < 0.05:
            opponent_type = "trustworthy"
        elif defection_rate > 0.9:
            opponent_type = "greedy"
        elif var_recent > 0.2 and 0.4 < defection_rate < 0.6:
            opponent_type = "random"
        elif n >= 5:

            tft_matches = 0
            check_limit = min(8, n - 1)
            for i in range(1, check_limit + 1):
                if opponent_history[i] == my_history[i - 1]:
                    tft_matches += 1
            if tft_matches >= check_limit * 0.8:
                opponent_type = "tit_for_tat"

        if opponent_type == "unknown" and n % 10 == 0 and n >= 15:

            forgiveness_count = sum(1 for i in range(1, min(n, 20))
                                    if i > 0 and my_history[i - 1] == 0 and opponent_history[i] == 1)
            if forgiveness_count >= 2 and overall_coop > 0.6:
                opponent_type = "generous_tit_for_tat"


            elif n >= 20:
                early_coop = sum(opponent_history[:n // 2]) / (n // 2)
                late_defect = 1 - (sum(opponent_history[n // 2:]) / (n - n // 2))
                if early_coop > 0.7 and late_defect > 0.4:
                    opponent_type = "exploitative"

    if overall_coop >= 0.95:
        return 1
    if overall_coop <= 0.05:
        return 0

    round_progress = n / rounds if rounds is not None else 0.5
    risk_tolerance = 0.3

    if round_progress < 0.3:
        risk_tolerance = 0.2
    elif round_progress > 0.7:
        risk_tolerance = 0.4

    if score_difference < -5:
        risk_tolerance += 0.1
    elif score_difference > 10:
        risk_tolerance -= 0.05

    if weighted_defections > 2.5:
        risk_tolerance += 0.15
        if recent_betrayal:
            return 0

    if opponent_type == "greedy":
        return 0

    if opponent_type == "trustworthy" and n > 20:
        return 1

    if opponent_type == "generous_tit_for_tat":

        if pseudo_random(n * 13) < 0.15:
            return 0
        return 1

    if opponent_type == "exploitative":

        if recent_coop < 0.7:
            return 0
        if pseudo_random(n * 11) < 0.35:
            return 0
        return 1

    if opponent_type == "random":
        return 0 if pseudo_random(n * 17) > 0.3 else 1

    if predicted_defection and pattern_confidence > risk_tolerance:
        return 0

    if recent_window.count(0) >= 3:
        return 0

    if n >= 2 and pseudo_random(n * 7919) < 0.15:
        if my_history[-1] == opponent_history[-1]:
            return my_history[-1]
        else:
            return 1 - my_history[-1]

    lower_threshold = 0.3
    upper_threshold = 0.7

    if weighted_defections > 2.0:
        lower_threshold += 0.1
        upper_threshold += 0.1

    if score_difference < -5:
        lower_threshold -= 0.1

    lower_threshold = max(0.1, min(0.5, lower_threshold))
    upper_threshold = max(0.5, min(0.9, upper_threshold))

    if combined_coop >= upper_threshold:
        return 1
    elif combined_coop <= lower_threshold:
        return 0
    else:

        prob_coop = sigmoid(2 * (combined_coop - 0.5))
        if pseudo_random(n * 101) < prob_coop:
            return 1
        else:
            return 0
