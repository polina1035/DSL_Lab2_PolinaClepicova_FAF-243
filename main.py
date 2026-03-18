"""
Main entry point for Laboratory Work #2.
Variant 7
"""
from finite_automaton import FiniteAutomaton

def main():
    # Define the automaton for Variant 7
    fa = FiniteAutomaton(
        states={'q0', 'q1', 'q2', 'q3'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): {'q1'},
            ('q1', 'b'): {'q2'},
            ('q2', 'b'): {'q3', 'q2'},   # non-deterministic transition
            ('q3', 'a'): {'q1'},
            ('q1', 'a'): {'q1'}
        },
        initial_state='q0',
        final_states={'q3'}
    )

    print("=== Variant 7 Finite Automaton ===")
    print(f"States: {fa.states}")
    print(f"Alphabet: {fa.alphabet}")
    print(f"Initial state: {fa.initial_state}")
    print(f"Final states: {fa.final_states}")
    print("Transitions:")
    for (s, a), targets in fa.transitions.items():
        print(f"  δ({s}, {a}) = {targets}")

    # Task 3b: Check determinism
    print("\n--- Task 3b: Determinism Check ---")
    if fa.is_deterministic():
        print("The automaton is DETERMINISTIC (DFA).")
    else:
        print("The automaton is NON-DETERMINISTIC (NFA).")

    # Task 3a: Convert FA to regular grammar
    print("\n--- Task 3a: FA to Regular Grammar ---")
    grammar = fa.to_regular_grammar()
    print(grammar)

    # Classify the grammar (Objective 1a from previous lab)
    print("--- Grammar Classification (Chomsky) ---")
    print("Grammar classification:", grammar.classify())

    # Task 3c: Convert NFA to DFA
    print("\n--- Task 3c: NFA to DFA Conversion ---")
    dfa = fa.to_dfa()
    print("DFA constructed. States (as sets of NFA states):")
    dfa.print_dfa()

    # Task 3d (Bonus): Graphical representation - output DOT
    print("\n--- Task 3d (Bonus): DOT representation of original NFA ---")
    print(fa.to_dot())

    print("\n--- DOT representation of converted DFA ---")
    print(dfa.to_dot())

if __name__ == "__main__":
    main()