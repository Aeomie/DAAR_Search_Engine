from astTree import RegExTree, Operation, RegEx
from nfa import State, NFA, epsilon_closure, nfa_match


# # Regex: "a"
# regex_str = "S(a|g|r)+on"
# parser = RegEx(regex_str)
# tree = parser.parse()
# nfa = NFA.tree_to_nfa(tree)
# print(nfa_match(nfa, "Saon"))  # True

"""
NFA Only
"""
# if __name__ == "__main__":
#     regex_str = input("Enter a regex: ")
#     parser = RegEx(regex_str)
#     try:
#         tree = parser.parse()
#         print("Parsed tree:", tree)
#         nfa = NFA.tree_to_nfa(tree)
#         while(1):
#             test_str = input("('exit' to quit, 'regex' to ask for another regex)\n Enter a string to test: ")
#             if test_str == 'exit':
#                 exit(0)
#             if test_str == 'regex':
#                 regex_str = input("Enter a regex: ")
#                 parser = RegEx(regex_str)
#                 try:
#                     tree = parser.parse()
#                     print("Parsed tree:", tree)
#                     nfa = NFA.tree_to_nfa(tree)
#                 except Exception as e:
#                     print("Error parsing regex:", e)
#                 continue
#             if nfa_match(nfa, test_str):
#                 print(f"The string '{test_str}' is accepted by the regex '{regex_str}'")
#             else:
#                 print(f"The string '{test_str}' is NOT accepted by the regex '{regex_str}'")
#     except Exception as e:
#         print("Error parsing regex:", e)

"""
DFA
"""

if __name__ == "__main__":
    regex_str = input("Enter a regex: ")
    parser = RegEx(regex_str)
    try:
        tree = parser.parse()
        print("Parsed tree:", tree)

        # Build NFA
        nfa = NFA.tree_to_nfa(tree)

        # Build DFA from NFA
        alphabet = NFA.get_alphabet(nfa)
        dfa_start, dfa_accepts = nfa.nfa_to_dfa(alphabet)

        while True:
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
                    alphabet = NFA.get_alphabet(nfa)
                    dfa_start, dfa_accepts = nfa.nfa_to_dfa(alphabet)
                except Exception as e:
                    print("Error parsing regex:", e)
                continue

            # Test with DFA
            if NFA.dfa_match(dfa_start, dfa_accepts, test_str):
                print(f"The string '{test_str}' is ACCEPTED by the regex '{regex_str}'")
            else:
                print(f"The string '{test_str}' is NOT accepted by the regex '{regex_str}'")

    except Exception as e:
        print("Error parsing regex:", e)