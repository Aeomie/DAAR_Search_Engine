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
                    text = f.read().replace("\n", " ")
                    if ignore_case:
                        text = text.lower()
                    out.write(text + " ")
    print(f"[+] All books merged into {output}")


def word_counter(file="merged.txt"):
    with open(file, encoding="utf-8") as f:
        return len(f.read().split())


def benchmark(algorithm, text, pattern, step=1000, max_words=50000):
    words = text.split()
    times = []

    for i in range(step, min(len(words), max_words) + 1, step):
        sample = " ".join(words[:i])
        start = time.perf_counter()

        # Choose the right match function
        if isinstance(algorithm, KMP):
            algorithm.match_kmp(sample)
        elif isinstance(algorithm, Boyer):
            algorithm.match_boyer(sample)
        elif isinstance(algorithm, DFA):
            algorithm.match_dfa(sample)

        end = time.perf_counter()
        times.append((i, end - start))
        print(f"{algorithm.__class__.__name__}: {i} words -> {end - start:.5f}s")

    return times


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
    p.add_argument("--step", type=int, default=1000,
                   help="Nombre de mots à ajouter à chaque itération.")
    p.add_argument("--max-words", type=int, default=50000,
                   help="Nombre maximal de mots à lire (par défaut 50000).")
    p.add_argument("-i", "--ignore-case", action="store_true",
                   help="Ignorer la casse (tout mettre en minuscules).")
    return p


def main():
    args = build_arg_parser().parse_args()

    pattern = args.pattern.lower() if args.ignore_case else args.pattern

    # Merge and prepare text
    merge_books(args.folder, ignore_case=args.ignore_case)
    text = open("merged.txt", encoding="utf-8").read()

    print(f"Number of words in the merged file {word_counter()}")
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

    # Run benchmark
    benchmark(algorithm, text, pattern, step=args.step, max_words=args.max_words)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
