def strategy_round_3(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    
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
        
    
    def select_next_opponent():
        
        standard_choice = opponent_id
        best_coop = -1.0
        
        for opp_id, opp_hist in opponents_history.items():
            if len(opp_hist) < 200:
                ratio = sum(opp_hist) / len(opp_hist) if opp_hist else 0.5
                
                if opp_id in my_history:
                    exploitation_factor = sum(1 for m, o in zip(my_history[opp_id], opp_hist) if m == 0 and o == 1)
                    exploitation_factor = exploitation_factor / len(opp_hist) if opp_hist else 0
                    
                    if exploitation_factor > 0.3:
                        ratio *= 0.9
                
                adjusted_ratio = ratio * 0.9 + 0.1 * (1.0 - abs(ratio - 0.5))
                if adjusted_ratio > best_coop:
                    best_coop = adjusted_ratio
                    standard_choice = opp_id
        
        
        if pseudo_random(n + opponent_id * 31) < 0.05:
            MIN_ROUNDS = 5
            special_choice = None
            best_score = -9999.0
            
            for opp_id, opp_hist in opponents_history.items():
                if len(opp_hist) < 200:  
                    
                    reliability = min(1.0, len(opp_hist) / MIN_ROUNDS) if opp_hist else 0.1
                    
                    if opp_hist:
                        coop_rate = sum(opp_hist) / len(opp_hist)
                        
                        
                        mean_opp = coop_rate
                        var_opp = sum((x - mean_opp) ** 2 for x in opp_hist) / len(opp_hist)
                        
                        
                        if len(my_history.get(opp_id, [])) > 0:
                            my_hist = my_history[opp_id]
                            total_payoff = 0
                            for m, o in zip(my_hist, opp_hist[:len(my_hist)]):
                                if m == 1 and o == 1:
                                    total_payoff += 3
                                elif m == 1 and o == 0:
                                    total_payoff += 0
                                elif m == 0 and o == 1:
                                    total_payoff += 5
                                else:
                                    total_payoff += 1
                            avg_payoff = total_payoff / len(my_hist)
                            payoff_factor = avg_payoff / 2.5  
                        else:
                            
                            payoff_factor = (3 * coop_rate**2 + 5 * coop_rate * (1 - coop_rate) + 1 * (1 - coop_rate)**2) / 2.5
                        
                        
                        score = reliability * (coop_rate * 0.6 + (1 - var_opp) * 0.2 + payoff_factor * 0.2)
                        
                        if score > best_score:
                            best_score = score
                            special_choice = opp_id
            
            return special_choice if special_choice is not None else standard_choice
        else:
            return standard_choice

    
    current_my_history = my_history.get(opponent_id, [])
    current_opponent_history = opponents_history.get(opponent_id, [])
    n = len(current_my_history)

    

    
    if n < 5:
        if n == 0:
            move = 1  
        elif n == 1:
            move = 1 if current_opponent_history[0] == 1 else 0  
        elif current_opponent_history[-1] == 0 and current_opponent_history[-2:].count(0) == 2:
            move = 0  
        else:
            move = 1
    else:
        
        my_score = 0
        opp_score = 0

        if n >= 10:
            for i in range(n):
                if current_my_history[i] == 1 and current_opponent_history[i] == 1:
                    my_score += 3
                    opp_score += 3
                elif current_my_history[i] == 1 and current_opponent_history[i] == 0:
                    my_score += 0
                    opp_score += 5
                elif current_my_history[i] == 0 and current_opponent_history[i] == 1:
                    my_score += 5
                    opp_score += 0
                else:
                    my_score += 1
                    opp_score += 1

        score_difference = my_score - opp_score

        
        betrayal_memory = 0
        recent_betrayal = False

        for i in range(max(1, n - 10), n):
            if i > 0 and current_my_history[i-1:i+1] == [1, 1] and current_opponent_history[i-1:i+1] == [0, 0]:
                betrayal_memory += 1
                recent_betrayal = True

        if betrayal_memory > 0 and n > 20:
            betrayal_memory = max(0, betrayal_memory - (n // 30))

        window_size = min(10, n)
        recent_window = current_opponent_history[-window_size:] if window_size > 0 else []

        
        weighted_defections = 0
        if n >= 5:
            weighted_defections = sum((0.8 ** i) * (1 - current_opponent_history[-(i+1)])
                                     for i in range(min(10, n)))

        
        pattern = None
        cycle_pattern = None
        predicted_defection = False
        pattern_confidence = 0.0

        if n > 10 and n % 4 == 0:
            pattern = detect_pattern(current_opponent_history)

            if n % 12 == 0 and n > 15:
                cycle_pattern = detect_cycle(current_opponent_history)
                if cycle_pattern and not pattern:
                    pattern = cycle_pattern
                    predicted_move = pattern[n % len(pattern)]
                    predicted_defection = (predicted_move == 0)
                    pattern_confidence = 0.65

            if n % 6 == 0 or pattern is None:
                ngram_move, ngram_confidence = ngram_analysis(current_opponent_history, 3)
                if ngram_move is not None and ngram_confidence > 0.65:
                    predicted_defection = (ngram_move == 0)
                    pattern_confidence = ngram_confidence

            if pattern and not cycle_pattern:
                predicted_move = pattern[0]
                predicted_defection = (predicted_move == 0)
                pattern_confidence = 0.7

        
        recent_coop = ema(recent_window, 0.3) if recent_window else 0.5
        overall_coop = sum(current_opponent_history) / n if n > 0 else 1.0
        combined_coop = 0.6 * recent_coop + 0.4 * overall_coop

        
        var_recent = 0.0
        if n >= 5:
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
                check_limit = min(8, n-1)
                for i in range(1, check_limit + 1):
                    if current_opponent_history[i] == current_my_history[i-1]:
                        tft_matches += 1
                if tft_matches >= check_limit * 0.8:
                    opponent_type = "tit_for_tat"

            
            if opponent_type == "unknown" and n >= 15:
                forgiveness_count = sum(1 for i in range(1, min(n, 20))
                                       if i > 0 and current_my_history[i-1] == 0 and current_opponent_history[i] == 1)
                if forgiveness_count >= 2 and overall_coop > 0.6:
                    opponent_type = "generous_tit_for_tat"
                elif n >= 20:
                    early_coop = sum(current_opponent_history[:n//2]) / (n//2)
                    late_defect = 1 - (sum(current_opponent_history[n//2:]) / (n - n//2))
                    if early_coop > 0.7 and late_defect > 0.4:
                        opponent_type = "exploitative"

        
        if overall_coop >= 0.95:
            move = 1
        elif overall_coop <= 0.05:
            move = 0
        else:
            
            risk_tolerance = 0.3

            
            if score_difference < -5:
                risk_tolerance += 0.1
            elif score_difference > 10:
                risk_tolerance -= 0.05

            
            if weighted_defections > 2.5:
                risk_tolerance += 0.15
                if recent_betrayal:
                    move = 0
                    return (move, select_next_opponent())

            
            if opponent_type == "greedy":
                move = 0
                return (move, select_next_opponent())

            if opponent_type == "trustworthy" and n > 20:
                move = 1
                return (move, select_next_opponent())

            if opponent_type == "generous_tit_for_tat":
                if pseudo_random(n * 13) < 0.15:
                    move = 0
                else:
                    move = 1
                return (move, select_next_opponent())

            if opponent_type == "exploitative":
                if recent_coop < 0.7:
                    move = 0
                elif pseudo_random(n * 11) < 0.35:
                    move = 0
                else:
                    move = 1
                return (move, select_next_opponent())

            if opponent_type == "random":
                move = 0 if pseudo_random(n * 17) > 0.3 else 1
                return (move, select_next_opponent())

            
            if predicted_defection and pattern_confidence > risk_tolerance:
                move = 0
                return (move, select_next_opponent())

            
            if recent_window.count(0) >= 3:
                move = 0
                return (move, select_next_opponent())

            
            if n >= 2 and pseudo_random(n * 7919) < 0.15:
                if current_my_history[-1] == current_opponent_history[-1]:
                    move = current_my_history[-1]
                else:
                    move = 1 - current_my_history[-1]
                return (move, select_next_opponent())

            
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
                move = 1
            elif combined_coop <= lower_threshold:
                move = 0
            else:
                
                prob_coop = sigmoid(2 * (combined_coop - 0.5))
                if pseudo_random(n * 101) < prob_coop:
                    move = 1
                else:
                    move = 0

    
    def select_next_opponent():
        
        standard_choice = opponent_id
        best_coop = -1.0
        
        for opp_id, opp_hist in opponents_history.items():
            if len(opp_hist) < 200:
                ratio = sum(opp_hist) / len(opp_hist) if opp_hist else 0.5
                
                if opp_id in my_history:
                    exploitation_factor = sum(1 for m, o in zip(my_history[opp_id], opp_hist) if m == 0 and o == 1)
                    exploitation_factor = exploitation_factor / len(opp_hist) if opp_hist else 0
                    
                    if exploitation_factor > 0.3:
                        ratio *= 0.9
                
                adjusted_ratio = ratio * 0.9 + 0.1 * (1.0 - abs(ratio - 0.5))
                if adjusted_ratio > best_coop:
                    best_coop = adjusted_ratio
                    standard_choice = opp_id
        
        
        if pseudo_random(n + opponent_id * 31) < 0.05:
            MIN_ROUNDS = 5
            special_choice = None
            best_score = -9999.0
            
            for opp_id, opp_hist in opponents_history.items():
                if len(opp_hist) < 200:  
                    
                    reliability = min(1.0, len(opp_hist) / MIN_ROUNDS) if opp_hist else 0.1
                    
                    if opp_hist:
                        coop_rate = sum(opp_hist) / len(opp_hist)
                        
                        
                        mean_opp = coop_rate
                        var_opp = sum((x - mean_opp) ** 2 for x in opp_hist) / len(opp_hist)
                        
                        
                        if len(my_history.get(opp_id, [])) > 0:
                            my_hist = my_history[opp_id]
                            total_payoff = 0
                            for m, o in zip(my_hist, opp_hist[:len(my_hist)]):
                                if m == 1 and o == 1:
                                    total_payoff += 3
                                elif m == 1 and o == 0:
                                    total_payoff += 0
                                elif m == 0 and o == 1:
                                    total_payoff += 5
                                else:
                                    total_payoff += 1
                            avg_payoff = total_payoff / len(my_hist)
                            payoff_factor = avg_payoff / 2.5  
                        else:
                            
                            payoff_factor = (3 * coop_rate**2 + 5 * coop_rate * (1 - coop_rate) + 1 * (1 - coop_rate)**2) / 2.5
                        
                        
                        score = reliability * (coop_rate * 0.6 + (1 - var_opp) * 0.2 + payoff_factor * 0.2)
                        
                        if score > best_score:
                            best_score = score
                            special_choice = opp_id
            
            return special_choice if special_choice is not None else standard_choice
        else:
            return standard_choice
    
    
    next_opponent = select_next_opponent()
    
    return (move, next_opponent)