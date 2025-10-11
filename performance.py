from __future__ import annotations
import os
import sys
import time
import argparse
from search_algorithms.kmp import KMP
from search_algorithms.nfa import NFA
from search_algorithms.dfa import DFA
from search_algorithms.boyer_moore import Boyer


def merge_books(folder="livres", output="merged.txt", ignore_case=False):
    with open(output, "w", encoding="utf-8") as out:
        for fname in os.listdir(folder):
            if fname.endswith(".txt"):
                with open(os.path.join(folder, fname), "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                    if ignore_case:
                        text = text.lower()
                    out.write(text.strip() + "\n\n")  # preserve lines + separate books
    print(f"[+] All books merged into {output}")



def word_counter(file="merged.txt"):
    with open(file, encoding="utf-8") as f:
        return len(f.read().split())

def line_counter(file="merged.txt"):
    with open(file, encoding="utf-8") as f:
        return sum(1 for _ in f)

def benchmark_by_words(algorithm, text, step=1000, max_words=50000):
    words = text.split()
    times = []
    occurences = 0
    for i in range(step, min(len(words), max_words) + 1, step):
        sample = " ".join(words[:i])
        start = time.perf_counter()

        count = 0
        # Choose the right match function
        if isinstance(algorithm, KMP):
            indexes , count = algorithm.match_kmp(sample)
        elif isinstance(algorithm, Boyer):
            indexes , count = algorithm.match_boyer(sample)
        elif isinstance(algorithm, DFA):
            indexes , count = algorithm.match_dfa(sample)

        occurences += count
        end = time.perf_counter()
        times.append((i, end - start))
        print(f"{algorithm.__class__.__name__}: {i} words -> {end - start:.5f}s")

    return times, occurences
def benchmark_by_lines(algorithm, file="merged.txt", max_lines=50000):
    """
    Benchmark the algorithm line by line, reading from the file.
    """
    times = []
    lines = []
    occurences = 0

    # Read all lines first
    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    for i in range(1, min(len(lines), max_lines) + 1):
        sample = "".join(lines[:i])  # combine first i lines
        start = time.perf_counter()
        count = 0
        # Choose the right match function
        if isinstance(algorithm, KMP):
            indexes , count = algorithm.match_kmp(sample)
        elif isinstance(algorithm, Boyer):
            indexes , count = algorithm.match_boyer(sample)
        elif isinstance(algorithm, DFA):
            indexes , count = algorithm.match_dfa(sample)

        occurences += count
        end = time.perf_counter()
        times.append((i, end - start))
        print(f"{algorithm.__class__.__name__}: {i} lines -> {end - start:.5f}s")

    return times, occurences


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pertest",
        description="Performance tester utilisant KMP, Boyer–Moore ou DFA (regex).",
        allow_abbrev=False,
    )
    p.add_argument("pattern", help="Pattern à chercher.")
    p.add_argument("-f", "--folder", default="livres",
                   help="Dossier contenant les fichiers texte à fusionner.")
    p.add_argument("-m", "--mode", choices=["kmp", "boyer", "regex"], default="regex",
                   help="Choisir le moteur (regex par défaut).")
    p.add_argument("-i", "--ignore-case", action="store_true",
                   help="Ignorer la casse (tout mettre en minuscules).")

    group = p.add_mutually_exclusive_group()
    group.add_argument("-l", "--lines", action="store_true", default=True,
                       help="Benchmark par lignes (mode par défaut).")
    group.add_argument("-w", "--words", action="store_true",
                       help="Benchmark par mots (active --step et --max-words).")

    p.add_argument("--max", type=int, default=50000,
                   help="Nombre maximal de trucs à lire soit mots soit lignes.")

    # Only relevant for word mode
    p.add_argument("--step", type=int, default=1000,
                   help="Nombre de mots à ajouter à chaque itération (uniquement en mode mots).")

    return p



def main():
    args = build_arg_parser().parse_args()

    # Default to line mode if neither flag is given
    if not (args.words or args.lines):
        args.lines = True

    pattern = args.pattern.lower() if args.ignore_case else args.pattern

    # Merge all book files
    merge_books(args.folder, ignore_case=args.ignore_case)

    # Read merged text
    text = open("merged.txt", encoding="utf-8").read()

    print(f"Number of words in the merged file: {word_counter()}")
    print(f"Number of lines in the merged file: {line_counter()}")

    # Select algorithm
    if args.mode == "kmp":
        algorithm = KMP(pattern)
    elif args.mode == "boyer":
        algorithm = Boyer(pattern)
    elif args.mode == "regex":
        algorithm = DFA(NFA(pattern))
    else:
        sys.stderr.write(f"[ERREUR] Mode inconnu : {args.mode}\n")
        return 2

    occurrence = 0
    # Run benchmark
    if args.words:
        # Step/max_words only relevant for word mode
        times, occurrence = benchmark_by_words(algorithm, text, step=args.step, max_words=args.max)
    elif args.lines:
        times, occurrence = benchmark_by_lines(algorithm, max_lines=args.max)

    if occurrence > 0:
        print(f"Total occurrences found: {occurrence}")
    else:
        print("No occurrences found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
