from astTree import RegExTree, Operation, RegEx
from nfa import extract_alphabet, enumerate_leaves, build_transition_table



if __name__ == "__main__":
    regex_str = input("Enter a regex: ")
    parser = RegEx(regex_str)
    tree = parser.parse()
    # Build NFA

