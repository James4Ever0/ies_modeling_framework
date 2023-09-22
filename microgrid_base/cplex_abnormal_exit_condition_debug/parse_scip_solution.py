
if __name__ == "__main__":
    for fname in ["sol.xml", "relaxed_scip.sol"]:
        print("parsing:", fname)
        with open(fname,'r') as f:
            content = f.read()
            solved, solution = parse_scip_solution_content(content)
            print("solved?", solved)
            if solved:
                print('solution:', str(solution)[:100]+"...")
            print("="*70)