from __future__ import annotations

import random
import os
import sys
import importlib.util
import inspect
from typing import Callable, Union
from pathlib import Path
import concurrent.futures
import time
import multiprocessing

# Add the root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# --- Benchmark Strategies & ACES Import ---
try:
    from aces import strategy as aces_strategy
except ImportError:
    print("WARNING: Could not import 'aces' strategy. Ensure aces.py is in the root directory.")
    def aces_strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
        print("ERROR: ACES strategy not found!")
        return 0

def always_cooperate(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return 1

def always_defect(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return 0

def tit_for_tat(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return opponent_history[-1] if opponent_history else 1

def random_strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return random.choice([0, 1])

# Store benchmark functions globally - these are usually pickleable
BENCHMARK_STRATEGIES_DICT = {
    "Alw. Coop.": always_cooperate,
    "Alw. Defect": always_defect,
    "Tit-for-Tat": tit_for_tat,
    "Random": random_strategy,
    "ACES": aces_strategy,
}

# --- Core Game Logic ---
def compute_score(my_move: int, opponent_move: int) -> tuple[int, int]:
    if my_move == 1 and opponent_move == 1: return 3, 3
    if my_move == 1 and opponent_move == 0: return 0, 5
    if my_move == 0 and opponent_move == 1: return 5, 0
    return 1, 1

def simulate_match(strategy_A: Callable, strategy_B: Callable, rounds: int) -> tuple[int, int]:
    history_A, history_B = [], []
    score_A, score_B = 0, 0
    for _ in range(rounds):
        try:
            move_A = strategy_A(list(history_A), list(history_B), rounds)
            move_B = strategy_B(list(history_B), list(history_A), rounds)

            if move_A not in [0, 1]: move_A = 0
            if move_B not in [0, 1]: move_B = 0

            history_A.append(move_A)
            history_B.append(move_B)
            pts_A, pts_B = compute_score(move_A, move_B)
            score_A += pts_A
            score_B += pts_B
        except Exception as e:
            # Silently handle errors by assuming both defect
            history_A.append(0)
            history_B.append(0)
            score_A += 1
            score_B += 1
    return score_A, score_B

# --- Strategy Validation (Helper for Main Process) ---
def _validate_strategy_file(file_path_str: str) -> bool:
    """
    Attempts to load and validate a strategy function from a file.
    Returns True if valid, False otherwise. Prints warnings on failure.
    """
    module_name = Path(file_path_str).stem
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path_str)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Temporarily add path for loading
            module_dir = str(Path(file_path_str).parent)
            original_sys_path = list(sys.path)
            if module_dir not in sys.path:
                 sys.path.insert(0, module_dir)
            if str(root_dir) not in sys.path: # Ensure root is also there
                 sys.path.insert(0, str(root_dir))

            spec.loader.exec_module(module)
            # Restore sys.path
            sys.path = original_sys_path

            if hasattr(module, "strategy"):
                strategy_func = getattr(module, "strategy")
                if callable(strategy_func):
                    sig = inspect.signature(strategy_func)
                    params = list(sig.parameters.keys())
                    # Check for exact parameter names
                    if params == ["my_history", "opponent_history", "rounds"]:
                        try:
                            # Basic test call
                            test_result = strategy_func([], [], None)
                            if isinstance(test_result, int) and test_result in [0, 1]:
                                return True # Strategy is valid
                            else:
                                print(f"VALIDATION WARNING: Invalid return value from {module_name}. Skipping.")
                        except Exception as e:
                            print(f"VALIDATION WARNING: Error testing strategy {module_name}: {e}. Skipping.")
                    else:
                        # More specific error for wrong parameters
                        print(f"VALIDATION WARNING: Invalid parameters in {module_name} (Expected ['my_history', 'opponent_history', 'rounds'], got {params}). Skipping.")
                else:
                    print(f"VALIDATION WARNING: 'strategy' in {module_name} is not callable. Skipping.")
            else:
                print(f"VALIDATION WARNING: No 'strategy' function found in {module_name}. Skipping.")
        else:
            print(f"VALIDATION WARNING: Could not create spec for {file_path_str}. Skipping.")

    except Exception as e:
        print(f"VALIDATION ERROR loading module {module_name} from {file_path_str}: {e}")

    return False # Failed validation

# --- Strategy Loading (Main Process - Validates and Returns Paths/Callables) ---
def load_strategy_references(folder: str | Path) -> dict[str, Union[Callable, str]]:
    """
    Validates strategies and loads references.
    Returns a dict mapping strategy name to either:
        - Callable: For benchmark strategies.
        - str: Absolute path to the .py file for *valid* dynamically loaded strategies.
    """
    strategy_refs: dict[str, Union[Callable, str]] = {}
    folder_path = Path(folder)
    if not folder_path.is_dir():
        print(f"ERROR: The strategies folder '{folder_path.resolve()}' does not exist or is not a directory.")
        return strategy_refs

    print(f"Scanning and validating strategies in: {folder_path.resolve()}")
    found_count = 0
    valid_count = 0
    skipped_count = 0

    for file_path_obj in folder_path.glob("*.py"):
        module_name = file_path_obj.stem
        if module_name == "__init__":
            continue

        found_count += 1
        file_path_str = str(file_path_obj.resolve())

        # Validate the strategy file *before* adding its path
        if _validate_strategy_file(file_path_str):
            strategy_refs[module_name] = file_path_str # Store path if valid
            valid_count += 1
        else:
            skipped_count += 1 # Validation failed, skip this strategy

    print(f"Found {found_count} potential dynamic files. Loaded {valid_count} valid strategies (skipped {skipped_count}).")

    # Add benchmark strategies (as callables)
    # Benchmarks are assumed valid and don't overwrite validated dynamic ones
    benchmarks_to_add = {k: v for k, v in BENCHMARK_STRATEGIES_DICT.items() if k not in strategy_refs}
    strategy_refs.update(benchmarks_to_add)

    return strategy_refs

# --- Worker Function (Loads from validated path) ---
def _load_strategy_from_path(file_path_str: str) -> Callable | None:
    """
    Loads the 'strategy' function from a given file path.
    Assumes the path has already been validated in the main process.
    Designed to run *within* a worker process.
    Returns the callable function or None if loading fails unexpectedly.
    """
    # Reduced error checking here as validation happened in main process
    try:
        module_name = Path(file_path_str).stem
        spec = importlib.util.spec_from_file_location(module_name, file_path_str)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Ensure necessary paths are available in the worker
            module_dir = str(Path(file_path_str).parent)
            worker_root_dir = str(Path(__file__).resolve().parent.parent)
            if module_dir not in sys.path:
                 sys.path.insert(0, module_dir)
            if worker_root_dir not in sys.path:
                 sys.path.insert(0, worker_root_dir)

            spec.loader.exec_module(module)
            if hasattr(module, "strategy") and callable(getattr(module, "strategy")):
                return getattr(module, "strategy") # Return the function
            else:
                 # This case should ideally not happen if validation worked
                 print(f"WORKER ERROR: Validated strategy {module_name} missing callable 'strategy' function unexpectedly.")
        else:
             print(f"WORKER ERROR: Could not create spec for validated path {file_path_str}.")

    except Exception as e:
        # Catch unexpected errors during loading in worker
        print(f"WORKER ERROR loading previously validated strategy from {file_path_str}: {e}")

    return None # Return None if loading failed unexpectedly

# --- Tournament Simulation ---
# Helper function for parallel execution - Accepts Paths or Callables
def run_trials_for_pair(pair_info: tuple[str, str, Union[Callable, str], Union[Callable, str], int, int]) -> tuple[str, str, int]:
    name_A, name_B, strategy_A_ref, strategy_B_ref, trials, rounds = pair_info
    pair_total_score_A = 0

    # Load strategy A if it's a path (should succeed if validation worked)
    strategy_A: Callable | None
    if isinstance(strategy_A_ref, str):
        strategy_A = _load_strategy_from_path(strategy_A_ref)
        if strategy_A is None:
            # Log error but return 0 - this indicates a problem post-validation
            print(f"WORKER: Unexpected failure loading validated strategy {name_A}. Skipping trials.")
            return name_A, name_B, 0
    else:
        strategy_A = strategy_A_ref # It's already a callable (benchmark)

    # Load strategy B if it's a path (should succeed if validation worked)
    strategy_B: Callable | None
    if isinstance(strategy_B_ref, str):
        strategy_B = _load_strategy_from_path(strategy_B_ref)
        if strategy_B is None:
            # Log error but return 0
            print(f"WORKER: Unexpected failure loading validated strategy {name_B}. Skipping trials.")
            return name_A, name_B, 0
    else:
        strategy_B = strategy_B_ref # It's already a callable (benchmark)

    # Run trials only if both strategies were successfully loaded/retrieved
    # This check is still needed in case of unexpected loading errors
    if strategy_A and strategy_B:
        for _ in range(trials):
            try:
                sA, _ = simulate_match(strategy_A, strategy_B, rounds)
                pair_total_score_A += sA
            except Exception as e:
                print(f"ERROR during match {name_A} vs {name_B} in worker: {e}. Skipping trial.")
                pass # Skip score addition for this trial

    return name_A, name_B, pair_total_score_A

def run_tournament(trials: int = 100, rounds: int = 100, strategies_folder: str | Path = "strategies", max_workers: int | None = None):
    start_time = time.time()

    # Load and VALIDATE strategy references (paths or callables)
    strategy_references = load_strategy_references(strategies_folder)

    # Only use the names of the successfully loaded/validated strategies
    names = list(strategy_references.keys())
    num_strategies = len(names)
    if num_strategies < 2:
        print("ERROR: Need at least two valid strategies to run a tournament.")
        return {}, {}, []

    print(f"\nRunning tournament with {num_strategies} valid strategies.")
    # Count benchmarks vs dynamic among the *valid* strategies
    num_benchmarks = sum(1 for ref in strategy_references.values() if callable(ref))
    num_dynamic = num_strategies - num_benchmarks
    print(f"({num_benchmarks} benchmarks, {num_dynamic} dynamic)")
    print(f"\nParameters: Trials={trials}, Rounds={rounds}, Max Workers={max_workers or os.cpu_count()}")

    # Prepare tasks for parallel execution - ONLY USING VALIDATED REFERENCES
    tasks = []
    for name_A in names: # Iterate only over valid names
        for name_B in names: # Iterate only over valid names
            tasks.append((
                name_A, name_B,
                strategy_references[name_A], # Pass path string or callable
                strategy_references[name_B], # Pass path string or callable
                trials, rounds
            ))

    # Initialize score structures only for valid strategies
    matchup_total_scores = {name: {opp: 0 for opp in names} for name in names}
    total_scores = {name: 0 for name in names}

    # Execute tasks in parallel
    print("Simulating matches...")
    processed_tasks = 0
    total_tasks = len(tasks)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_trials_for_pair, task) for task in tasks]
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
                processed_tasks += 1
                if processed_tasks % 100 == 0 or processed_tasks == total_tasks:
                    print(f"  Processed {processed_tasks}/{total_tasks} matchups...", end='\r')
            except Exception as e:
                print(f"\nERROR retrieving result from worker: {e}")

    print("\nSimulation complete.")

    # Process results
    successful_results = 0
    for name_A, name_B, pair_total_score_A in results:
        # Check if names are in the valid list before assigning scores
        if name_A in names and name_B in names:
             matchup_total_scores[name_A][name_B] = pair_total_score_A
             total_scores[name_A] += pair_total_score_A
             successful_results +=1
        # else: # Don't warn if a worker failed unexpectedly on a validated strategy
             # print(f"Internal Warning: Received result for invalid/unexpected pair ({name_A}, {name_B})")

    print(f"Processed {successful_results} valid matchup results.")

    # Calculate averages and leaderboard (only for valid strategies)
    average_matchup_score = {name: {} for name in names}
    match_count = {name: num_strategies * trials for name in names}

    for name_A in names:
        for name_B in names:
            average_matchup_score[name_A][name_B] = matchup_total_scores[name_A][name_B] / trials if trials > 0 else 0

    leaderboard = {}
    for name in names:
        total_matches_played = match_count[name]
        current_total_score = total_scores.get(name, 0) # Use .get for safety
        leaderboard[name] = {
            "total_score": current_total_score / trials if trials > 0 else 0,
            "avg_score_per_match": current_total_score / total_matches_played if total_matches_played > 0 else 0
        }

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]["avg_score_per_match"], reverse=True)

    end_time = time.time()
    print(f"\nTournament finished in {end_time - start_time:.2f} seconds.")

    return average_matchup_score, leaderboard, sorted_leaderboard

# --- Result Printing ---
def print_results(average_match_score, leaderboard, sorted_leaderboard):
    names = list(average_match_score.keys())
    if not names:
        print("No results to print.")
        return

    max_name_len_display = 18
    display_names = {name: (name[:max_name_len_display-2] + '..') if len(name) > max_name_len_display else name for name in names}

    print("\n=== Leaderboard ===")
    if sorted_leaderboard:
        max_name_len_lb = max(len(name) for name, _ in sorted_leaderboard)
        max_total_score_len = max(len(f"{leaderboard.get(name, {'total_score': 0})['total_score']:.0f}") for name in names) if names else 10
    else:
        max_name_len_lb = 20
        max_total_score_len = 10

    print("Place".ljust(7) + "Strategy".ljust(max_name_len_lb + 2) + "Avg Score/Trial".ljust(max_total_score_len + 12) + "Avg Score/Match")
    print("-" * (7 + max_name_len_lb + 2 + max_total_score_len + 5 + 22))
    for i, (name, scores) in enumerate(sorted_leaderboard):
        place = i + 1
        print(f"{place}".ljust(7) +
              name.ljust(max_name_len_lb + 2) +
              f"{scores.get('total_score', 0):.0f}".ljust(max_total_score_len + 12) +
              f"{scores.get('avg_score_per_match', 0.0):.3f}")

# --- Main Execution ---
if __name__ == "__main__":
    # --- Log multiprocessing start method ---
    print(f"INFO: Using multiprocessing start method '{multiprocessing.get_start_method()}'.")

    default_trials = 200
    default_rounds = 100
    default_strategies_folder = root_dir / "strategies"

    trials = default_trials
    rounds = default_rounds
    strategies_folder = default_strategies_folder
    max_workers = None

    if not strategies_folder.is_dir():
        print(f"ERROR: Strategies folder not found: {strategies_folder}")
        sys.exit(1)

    avg_matchup, leaderboard, sorted_lb = run_tournament(
        trials=trials,
        rounds=rounds,
        strategies_folder=strategies_folder,
        max_workers=max_workers
    )

    if avg_matchup:
        print_results(avg_matchup, leaderboard, sorted_lb)
    else:
        print("Tournament did not produce results (or no valid strategies found).")
