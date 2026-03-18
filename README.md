# Laboratory Work #2: Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy

**Course:** Formal Languages & Finite Automata  
**Author:** [Your Name]  
**Variant:** 7  
**Repository:** [Link to your GitHub repository]

---

## Table of Contents
1. [Theory](#theory)
2. [Objectives](#objectives)
3. [Implementation Description](#implementation-description)
4. [Code Snippets](#code-snippets)
5. [Challenges and Difficulties](#challenges-and-difficulties)
6. [Conclusions / Results](#conclusions--results)
7. [References](#references)

---

## Theory

### Finite Automata
A **finite automaton (FA)** is an abstract machine used to recognize patterns within input taken from a finite alphabet. Formally, an FA is a 5-tuple $M = (Q, \Sigma, \delta, q_0, F)$ where:
* $Q$ is a finite set of **states**.
* $\Sigma$ is a finite **input alphabet**.
* $\delta : Q \times \Sigma \to \mathcal{P}(Q)$ is the **transition function** (for an NFA) or $\delta : Q \times \Sigma \to Q$ (for a DFA).
* $q_0 \in Q$ is the **initial state**.
* $F \subseteq Q$ is the set of **final (accepting) states**.

### Determinism vs. Non‑determinism
* **Deterministic Finite Automaton (DFA):** has exactly one transition for each state and each input symbol.
* **Non‑deterministic Finite Automaton (NFA):** may have zero, one, or multiple transitions for a given state and symbol.

### Conversion from NFA to DFA
Every NFA can be transformed into an equivalent DFA using the **subset construction** (powerset construction) algorithm. The core idea is that a single state in the DFA represents a *set* of states in the NFA.

### Chomsky Hierarchy
Grammars are classified into four levels:
* **Type‑0:** Unrestricted.
* **Type‑1:** Context‑sensitive.
* **Type‑2:** Context‑free.
* **Type‑3:** Regular. Regular grammars correspond exactly to languages recognized by finite automata.



---

## Objectives

1. Extend the `Grammar` class to include a method that classifies a grammar according to the **Chomsky hierarchy**.
2. For the given **Variant 7**:
    * Convert the finite automaton into an equivalent regular grammar.
    * Determine whether the automaton is deterministic or non‑deterministic.
    * Implement the conversion from NFA to DFA.
    * (Optional) Represent the automaton graphically using Graphviz (DOT).

---

## Implementation Description

The project is implemented in **Python** using an Object-Oriented approach.

### `Grammar` Class
* **Method `classify()`:** Checks production rules to determine the grammar type. It validates if the grammar is right-linear or left-linear (Type-3), context-free (Type-2), etc.

### `FiniteAutomaton` Class
* **Method `is_deterministic()`:** Scans the transition table. If any `(state, symbol)` pair results in multiple target states, it flags the FA as non-deterministic.
* **Method `to_regular_grammar()`:** Converts transitions into production rules (e.g., $\delta(q_0, a) = q_1$ becomes $q_0 \to a q_1$).
* **Method `to_dfa()`:** Implements subset construction. It uses `frozenset` to track combinations of NFA states that form new DFA states.
* **Method `to_dot()`:** Exports the FA structure to DOT format for visualization.

---

## Code Snippets

### 1. NFA to DFA Conversion (Subset Construction)
```python
def to_dfa(self):
    from collections import deque
    start_set = frozenset([self.initial_state])
    dfa_states = {start_set}
    dfa_transitions = {}
    queue = deque([start_set])

    while queue:
        current = queue.popleft()
        for symbol in self.alphabet:
            reachable = set()
            for state in current:
                targets = self.transitions.get((state, symbol), set())
                reachable.update(targets)
            
            target_set = frozenset(reachable) if reachable else frozenset()
            dfa_transitions[(current, symbol)] = target_set
            
            if target_set not in dfa_states:
                dfa_states.add(target_set)
                queue.append(target_set)

    dfa_final = {s for s in dfa_states if any(q in self.final_states for q in s)}
    return FiniteAutomaton(states=dfa_states, transitions=dfa_transitions, ...)
