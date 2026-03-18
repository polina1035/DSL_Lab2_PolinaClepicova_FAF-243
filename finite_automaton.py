"""
FiniteAutomaton class for representing and manipulating finite automata.
"""
from collections import deque
from grammar import Grammar

class FiniteAutomaton:
    """Represents a finite automaton (could be NFA or DFA)."""
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        # transitions: dict (state, symbol) -> set of target states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def is_deterministic(self):
        """Returns True if the FA is deterministic, False otherwise."""
        for (state, symbol), targets in self.transitions.items():
            if len(targets) != 1:
                return False
        # Also ensure that for every state and every symbol there is exactly one transition
        # (if a transition is missing, it's also non-deterministic because DFA requires total transition function)
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions or len(self.transitions[(state, symbol)]) != 1:
                    return False
        return True

    def to_regular_grammar(self):
        """Converts the FA to a right-linear regular grammar."""
        productions = {state: [] for state in self.states}
        for (state, symbol), targets in self.transitions.items():
            for t in targets:
                productions[state].append(symbol + t)
        for f in self.final_states:
            productions[f].append('ε')
        return Grammar(
            non_terminals=self.states,
            terminals=self.alphabet,
            productions=productions,
            start_symbol=self.initial_state
        )

    def to_dfa(self):
        """Converts an NFA to an equivalent DFA using subset construction."""
        # Initial DFA state is frozenset containing the NFA start state
        start_set = frozenset([self.initial_state])
        dfa_states = {start_set}
        dfa_transitions = {}  # key: (dfa_state, symbol) -> dfa_state (frozenset)
        queue = deque([start_set])

        while queue:
            current = queue.popleft()
            for symbol in self.alphabet:
                # Compute the set of NFA states reachable from any state in current on symbol
                reachable = set()
                for state in current:
                    targets = self.transitions.get((state, symbol), set())
                    reachable.update(targets)
                target_set = frozenset(reachable) if reachable else frozenset()  # empty set as dead state
                dfa_transitions[(current, symbol)] = target_set
                if target_set not in dfa_states:
                    dfa_states.add(target_set)
                    queue.append(target_set)

        # Determine final states: any DFA state that contains at least one original final state
        dfa_final = {s for s in dfa_states if any(q in self.final_states for q in s)}

        # Create the DFA object. States are frozensets; we'll keep them as is.
        # For printing we may want to rename them for readability.
        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            initial_state=start_set,
            final_states=dfa_final
        )

    def to_dot(self):
        """Generates a DOT description of the automaton."""
        lines = ["digraph FA {", "  rankdir=LR;", "  node [shape = circle];"]
        # Define states
        for state in self.states:
            shape = "doublecircle" if state in self.final_states else "circle"
            # If state is a frozenset, we need a readable name
            if isinstance(state, frozenset):
                state_name = self._set_to_str(state)
            else:
                state_name = str(state)
            lines.append(f'  "{state_name}" [shape={shape}];')
        # Start arrow
        start_name = self._set_to_str(self.initial_state) if isinstance(self.initial_state, frozenset) else str(self.initial_state)
        lines.append(f'  start [shape=point];')
        lines.append(f'  start -> "{start_name}";')
        # Transitions
        for (s, a), targets in self.transitions.items():
            # s may be frozenset, a is symbol, targets may be a set or a single target (frozenset in DFA)
            if isinstance(s, frozenset):
                s_name = self._set_to_str(s)
            else:
                s_name = str(s)

            # In DFA, targets is a frozenset (a single DFA state)
            if isinstance(targets, frozenset):
                t_name = self._set_to_str(targets) if targets else "∅"
                lines.append(f'  "{s_name}" -> "{t_name}" [label="{a}"];')
            else:
                # NFA case: targets is a set of states
                for t in targets:
                    t_name = str(t)
                    lines.append(f'  "{s_name}" -> "{t_name}" [label="{a}"];')
        lines.append("}")
        return "\n".join(lines)

    def _set_to_str(self, s):
        """Convert a frozenset of state names to a readable string like '{q0,q1}'."""
        if not s:
            return "∅"
        return "{" + ",".join(sorted(str(x) for x in s)) + "}"

    def print_dfa(self):
        """Prints the DFA in a readable table format."""
        print("DFA States:")
        # Create mapping from frozenset to a short name for readability
        state_map = {}
        for i, state in enumerate(self.states):
            if not state:
                name = "∅"
            else:
                name = "{" + ",".join(sorted(str(x) for x in state)) + "}"
            state_map[state] = name
        # Print transition table
        print("State\t" + "\t".join(self.alphabet))
        for state in sorted(self.states, key=lambda s: (len(s), str(s))):
            row = state_map[state]
            for sym in self.alphabet:
                target = self.transitions.get((state, sym), frozenset())
                row += "\t" + state_map[target]
            # Mark final states
            if state in self.final_states:
                row += "  (final)"
            print(row)