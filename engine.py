from astTree import RegExTree, Operation, RegEx
from nfa import State, NFA

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

def nfa_match(nfa : 'NFA', string: str):
    """Return True if the NFA accepts the string."""
    current_states = epsilon_closure({nfa.start_state})

    for char in string:
        next_states = set()
        for state in current_states:
            if char in state.transitions:
                next_states.update(state.transitions[char])
        current_states = epsilon_closure(next_states)

    return nfa.accept_states in current_states


# Regex: "a"
regex_str = "a+"
parser = RegEx(regex_str)
tree = parser.parse()
nfa = NFA.tree_to_nfa(tree)
print(nfa_match(nfa, "aaaaaa"))  # True
