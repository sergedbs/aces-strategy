# ok_boomerang.py
# Stage 1 algorithm for the Iterated Prisoner’s Dilemma tournament


def strategy(my_history: list[int],
             opponent_history: list[int],
             rounds: int | None) -> int:
    """
    OK Boomerang (Windowed Regret + Forgiveness)

    • Cooperate on the very first move.
    • Use a sliding window (≈10 % of planned rounds, capped 1–20) of the
      opponent’s recent moves to compute their defection ratio.
    • Decision rules:
        – defect_ratio ≤ 0.30  → cooperate (1)
        – defect_ratio ≥ 0.70  → defect   (0)
        – otherwise play tempered tit‑for‑tat:
            • copy opponent’s last move
            • but if both defected last round and overall defect_ratio < 0.50,
              offer forgiveness and cooperate.
    Returns 1 for cooperation or 0 for defection.
    """
    COOP_THRESHOLD = 0.30  # cooperate if opponent’s defection rate ≤ 30 %
    DEFECT_THRESHOLD = 0.70  # defect if opponent’s defection rate ≥ 70 %
    FORGIVE_THRESHOLD = 0.50  # allow forgiveness when overall rate < 50 %
    WINDOW_MIN, WINDOW_MAX = 1, 20  # sliding‑window size limits

    # First round: cooperate
    if not my_history:
        return 1

    # Determine sliding‑window size
    if rounds is None:
        window = 10  # fallback when total rounds unknown
    else:
        window = max(WINDOW_MIN, min(WINDOW_MAX, rounds // 10 or 1))

    recent = opponent_history[-window:]
    defect_ratio = recent.count(0) / len(recent)

    if defect_ratio <= COOP_THRESHOLD:
        return 1
    if defect_ratio >= DEFECT_THRESHOLD:
        return 0

    last_opponent_move = opponent_history[-1]

    # Forgiveness after mutual defection
    if (len(my_history) >= 2
            and my_history[-1] == 0
            and last_opponent_move == 0
            and defect_ratio < FORGIVE_THRESHOLD):
        return 1

    # Tempered tit‑for‑tat
    return last_opponent_move
