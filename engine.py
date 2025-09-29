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


# # Regex: "a"
# regex_str = "S(a|g|r)+on"
# parser = RegEx(regex_str)
# tree = parser.parse()
# nfa = NFA.tree_to_nfa(tree)
# print(nfa_match(nfa, "Saon"))  # True
if __name__ == "__main__":
    regex_str = input("Enter a regex: ")
    parser = RegEx(regex_str)
    try:
        tree = parser.parse()
        print("Parsed tree:", tree)
        nfa = NFA.tree_to_nfa(tree)
        while(1):
            test_str = input("('exit' to quit, 'regex' to ask for another regex)\n Enter a string to test: ")
            if test_str == 'exit':
                exit(0)
            if test_str == 'regex':
                regex_str = input("Enter a regex: ")
                parser = RegEx(regex_str)
                try:
                    tree = parser.parse()
                    print("Parsed tree:", tree)
                    nfa = NFA.tree_to_nfa(tree)
                except Exception as e:
                    print("Error parsing regex:", e)
                continue
            if nfa_match(nfa, test_str):
                print(f"The string '{test_str}' is accepted by the regex '{regex_str}'")
            else:
                print(f"The string '{test_str}' is NOT accepted by the regex '{regex_str}'")
    except Exception as e:
        print("Error parsing regex:", e)