from nfa import NFA
from astTree import RegEx, RegExTree, Operation

class DFA:
    def __init__(self, nfa: NFA):
        self.nfa = nfa
        self.alphabet = [s for s in nfa.alphabet if s != 'ε']
        self.start_state = None
        self.final_states = set()
        self.transitions = {}
        self.build_dfa()

    # -----------------------------
    # Epsilon closure
    # -----------------------------
    def epsilon_closure(self, states):
        if isinstance(states, str):
            states = {states}

        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for symbol, targets in self.nfa.transitions.get(state, {}).items():
                if symbol == 'ε':
                    for t in targets:
                        if t not in closure:
                            closure.add(t)
                            stack.append(t)
        return closure

    # -----------------------------
    # Merge transitions for multiple states
    # -----------------------------
    def merge_states_transitions(self, states):
        transitions = {}
        for state in states:
            if state == self.nfa.final_state:
                self.final_states.add(frozenset(states))
            if state == self.nfa.start_state:
                self.start_state = frozenset(states)
            for symbol, targets in self.nfa.transitions.get(state, {}).items():
                if symbol == 'ε':
                    continue
                if symbol not in transitions:
                    transitions[symbol] = set()
                transitions[symbol].update(targets)
        return transitions

    # -----------------------------
    # Build DFA
    # -----------------------------
    def build_dfa(self):
        start_closure = self.epsilon_closure(self.nfa.start_state)
        self.start_state = frozenset(start_closure)

        queue = [self.start_state]
        visited = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            current_transitions = self.merge_states_transitions(current)
            self.transitions[current] = {}

            for symbol in self.alphabet:
                # All possible NFA states reachable via this symbol
                next_states = set()
                for s in current:
                    targets = self.nfa.transitions.get(s, {}).get(symbol, [])
                    next_states.update(targets)

                # Take epsilon closure of all those
                if next_states:
                    closure = self.epsilon_closure(next_states)
                    closure_frozen = frozenset(closure)
                    self.transitions[current][symbol] = closure_frozen

                    if closure_frozen not in visited and closure_frozen not in queue:
                        queue.append(closure_frozen)

        return self.transitions

    # -----------------------------
    # Display DFA Transition Table
    # -----------------------------
    def display_transition_table(self):
        print("\n=== DFA Transition Table ===")
        print(f"Start state: {set(self.start_state)}")
        print(f"Final states: {[set(s) for s in self.final_states]}\n")

        header = f"{'State':<30} | " + " | ".join(f"{s:<15}" for s in self.alphabet)
        print(header)
        print("-" * len(header))

        for state, trans in self.transitions.items():
            # Pretty state label
            state_label = ",".join(sorted(state))
            marker = ""
            if state == self.start_state:
                marker += "*"
            if state in self.final_states:
                marker += ">"

            row = f"{state_label:<28}{marker:<2} | "

            for symbol in self.alphabet:
                targets = trans.get(symbol, set())
                if not targets:
                    targets_str = "∅"
                else:
                    targets_str = ",".join(sorted(targets))
                row += f"{targets_str:<15} | "

            print(row)

        print("\n* for start state, > for final state")

    # -----------------------------
    # Match words
    # -----------------------------
    def match_dfa(self, word: str) -> bool:
        current_state = self.start_state
        for char in word:
            if char not in self.alphabet:
                raise Exception(f"Character '{char}' not in DFA alphabet")
            next_state = self.transitions.get(current_state, {}).get(char)
            if not next_state:
                return False
            current_state = next_state
        return current_state in self.final_states

if __name__ == "__main__":
    regex_str = input("Enter a regex: ")
    parser = RegEx(regex_str)

    try:
        tree = parser.parse()
        nfa = NFA(tree)
        nfa.display_transition_table()

        dfa = DFA(nfa)
        dfa.display_transition_table()
        while True:
            word = input("(exit) to exit \n"
                         "Enter a word to match:")
            if word == "exit ":
                break
            if dfa.match_dfa(word):
                print(f"The word '{word}' is accepted by the DFA.")
            else:
                print(f"The word '{word}' is NOT accepted by the DFA.")

    except Exception as e:
        print("Error:", e)
