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


