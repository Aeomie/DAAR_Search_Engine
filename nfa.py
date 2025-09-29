from regex import RegEx, RegExTree, Operation


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

    def tree_to_nfa(self, tree : RegExTree) -> 'NFA':
        if tree.root == Operation.CONCAT:
            left = self.tree_to_nfa(tree.subTrees[0])
            right = self.tree_to_nfa(tree.subTrees[1])
            left.accept_states.add_epsilon(right.start_state)
            return NFA(left.start_state, right.accept_states)
        elif tree.root == Operation.ALTERN:
            left = self.tree_to_nfa(tree.subTrees[0])
            right = self.tree_to_nfa(tree.subTrees[1])
            start = State()
            accept = State()
            start.add_epsilon(left.start_state, right.start_state)
            left.accept_states.add_epsilon(accept)
            right.accept_states.add_epsilon(accept)
            return NFA(start, accept)

        elif tree.root == Operation.ETOILE:
            sub_nfa = self.tree_to_nfa(tree.subTrees[0])
            start = State()
            accept = State()
            start.add_epsilon(sub_nfa.start_state, accept)
            sub_nfa.accept_states.add_epsilon(sub_nfa.start_state, accept)
            return NFA(start, accept)

        elif tree.root == Operation.PLUS:
            sub_nfa = self.tree_to_nfa(tree.subTrees[0])
            start = State()
            accept = State()
            start.add_epsilon(sub_nfa.start_state)
            sub_nfa.accept_states.add_epsilon(sub_nfa.start_state, accept)
            return NFA(start, accept)

