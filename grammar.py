"""
Grammar class for representing and classifying formal grammars.
"""

class Grammar:
    """Represents a formal grammar, capable of classifying itself in the Chomsky hierarchy."""
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions  # dict: non_terminal -> list of right-hand sides (strings)
        self.start_symbol = start_symbol

    def classify(self):
        """
        Classifies the grammar according to the Chomsky hierarchy.
        Returns a string describing the type.
        """
        # Check if grammar is regular (Type-3) – right-linear form: A -> aB or A -> a or A -> ε
        is_regular = True
        for nt, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if rhs == 'ε':
                    continue
                # Right-linear: exactly one terminal possibly followed by one non-terminal
                if len(rhs) == 1:
                    if rhs not in self.terminals:
                        is_regular = False
                        break
                elif len(rhs) == 2:
                    if rhs[0] not in self.terminals or rhs[1] not in self.non_terminals:
                        is_regular = False
                        break
                else:
                    is_regular = False
                    break
            if not is_regular:
                break

        if is_regular:
            return "Type 3 (Regular)"

        # Check if grammar is context-free (Type-2): left-hand side is a single non-terminal
        is_cf = True
        for nt in self.productions:
            if nt not in self.non_terminals:
                is_cf = False
                break
        if is_cf:
            return "Type 2 (Context-Free)"

        # Check if grammar is context-sensitive (Type-1): all productions satisfy |α| <= |β| except possibly S->ε
        is_cs = True
        for nt, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if rhs == 'ε' and nt == self.start_symbol:
                    continue  # allowed
                if len(nt) > len(rhs):  # left side longer than right side violates non-contracting
                    is_cs = False
                    break
            if not is_cs:
                break
        if is_cs:
            return "Type 1 (Context-Sensitive)"

        return "Type 0 (Unrestricted)"

    def __str__(self):
        res = f"Grammar(start={self.start_symbol})\n"
        res += "Productions:\n"
        for nt in sorted(self.productions):
            for rhs in self.productions[nt]:
                res += f"  {nt} -> {rhs}\n"
        return res