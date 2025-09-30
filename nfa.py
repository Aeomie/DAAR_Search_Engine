from astTree import RegEx, RegExTree, Operation

class State:
    def __init__(self):
        self.transitions = {}  # char -> set of states
        self.epsilon_transitions = set()  # set of states

    def add_transition(self, char, state):
        if char not in self.transitions:
            self.transitions[char] = set()
        self.transitions[char].add(state)

    def add_epsilon(self, *states):
        self.epsilon_transitions.update(states)


class NFA:
    def __init__(self, start_state: State, accept_states: State):
        self.start_state = start_state
        self.accept_states = accept_states


    @staticmethod
    def tree_to_nfa(tree : RegExTree) -> 'NFA':
        if tree.root == Operation.CONCAT:
            left = NFA.tree_to_nfa(tree.subTrees[0])
            right = NFA.tree_to_nfa(tree.subTrees[1])
            left.accept_states.add_epsilon(right.start_state)
            return NFA(left.start_state, right.accept_states)
        elif tree.root == Operation.ALTERN:
            left = NFA.tree_to_nfa(tree.subTrees[0])
            right = NFA.tree_to_nfa(tree.subTrees[1])
            start = State()
            accept = State()
            start.add_epsilon(left.start_state, right.start_state)
            left.accept_states.add_epsilon(accept)
            right.accept_states.add_epsilon(accept)
            return NFA(start, accept)

        elif tree.root == Operation.ETOILE:
            sub_nfa = NFA.tree_to_nfa(tree.subTrees[0])
            start = State()
            accept = State()
            start.add_epsilon(sub_nfa.start_state, accept)
            sub_nfa.accept_states.add_epsilon(sub_nfa.start_state, accept)
            return NFA(start, accept)

        elif tree.root == Operation.PLUS:
            sub_nfa = NFA.tree_to_nfa(tree.subTrees[0])
            start = State()
            accept = State()
            start.add_epsilon(sub_nfa.start_state)
            sub_nfa.accept_states.add_epsilon(sub_nfa.start_state, accept)
            return NFA(start, accept)
        elif isinstance(tree.root, str):
            # ← this is critical
            start = State()
            accept = State()
            start.add_transition(tree.root, accept)
            return NFA(start, accept)

        else:
            raise ValueError(f"Unsupported tree node: {tree.root}")

    def nfa_to_dfa(self, alphabet):
        start_set = epsilon_closure({self.start_state})
        dfa_states = {frozenset(start_set): State()}  # map NFA sets → DFA state
        unmarked = [frozenset(start_set)]  # DFA states to process
        dfa_start = dfa_states[frozenset(start_set)]

        while unmarked:
            current_set = unmarked.pop()
            current_dfa_state = dfa_states[current_set]

            for char in alphabet:
                # find all NFA states reachable from current_set via char
                next_set = set()
                for nfa_state in current_set:
                    if char in nfa_state.transitions:
                        next_set.update(nfa_state.transitions[char])
                next_set = epsilon_closure(next_set)
                frozen_next = frozenset(next_set)
                if frozen_next not in dfa_states:
                    dfa_states[frozen_next] = State()
                    unmarked.append(frozen_next)
                # add DFA transition
                current_dfa_state.add_transition(char, dfa_states[frozen_next])

        # determine DFA accepting states
        dfa_accepts = {state for nfa_set, state in dfa_states.items() if self.accept_states in nfa_set}

        return dfa_start, dfa_accepts

    def dfa_match(dfa_start, dfa_accepts, string):
        current_state = dfa_start
        for char in string:
            if char not in current_state.transitions:
                return False
            # deterministic → only one next state
            current_state = next(iter(current_state.transitions[char]))
        return current_state in dfa_accepts

    def get_alphabet(nfa):
        seen = set()
        stack = [nfa.start_state]
        visited = set()

        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)

            for char, next_states in state.transitions.items():
                seen.add(char)
                stack.extend(next_states)

            stack.extend(state.epsilon_transitions)

        return seen

def epsilon_closure(states):
    """Return the set of states reachable from `states` via epsilon moves."""
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for next_state in state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def nfa_match(nfa: 'NFA', string: str):
    """Return True if the NFA accepts the string."""
    current_states = epsilon_closure({nfa.start_state})

    for char in string:
        next_states = set()
        for state in current_states:
            if char in state.transitions:
                next_states.update(state.transitions[char])
        current_states = epsilon_closure(next_states)

    return nfa.accept_states in current_states