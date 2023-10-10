from swiplserver import PrologMQI, PrologThread

prolog_file_path = "arithmatic_prolog.pro"
import rich

with PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        prolog_thread.query(f'["{prolog_file_path}"].')
        # result = prolog_thread.query(f"solve(X).")
        # check solveable?
        result = prolog_thread.query(f"once(solve(X)).") # to quit early.
        # result = prolog_thread.query(f"solve(X).")
        # result_false = prolog_thread.query(f"solve_false(X).")
        result_false = prolog_thread.query(f"once(solve_false(X)).") # still False.
        rich.print(result)
        rich.print(result_false) # nothing returned.
