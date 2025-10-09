
from kmp import KMP
from boyer_moore import Boyer

def engine(pattern:str , file_to_run:str, mode:str):
    # Build NFA
    matcher = None
    match mode:
        case "kmp":
            matcher = KMP(pattern)
        case "boyer":
            matcher = Boyer(pattern)
    # Here you would typically run the NFA against the input file
    # For demonstration purposes, we will just print the structures
    print("NFA built successfully.")
    with open(file_to_run, 'r', encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f,start=1):
            #print("Processing lines:", line.strip())
            # Here you would implement the NFA matching logic
            # For now, we will just print the line
            indexes =[]
            count = 0
            line = line.strip().lower()
            match mode:
                case "kmp":
                    indexes, count = matcher.kmp(line)
                case "boyer":
                    indexes, count = matcher.match_boyer(line)

            if count > 0:
                print(f"Line {i}: Total matches found: {count}")
                print(f"Indexes of matches: {indexes}")


if __name__ == "__main__":
    input_str = input("Enter the file_name: ")
    mode_str = input("Enter the mode (kmp/boyer): ")
    pattern = input("Enter the pattern: ").lower()
    engine(pattern, input_str, mode_str)



