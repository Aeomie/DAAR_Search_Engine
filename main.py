#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import sys
import os
import re
import argparse
from typing import Iterable, Iterator, Optional, Tuple

# ============================================================
# Démo : moteur temporaire basé sur re.search
# ============================================================

DEMO: bool = False
_DEMO_STATE = {"pattern": None}

# ============================================================
# Stubs
# ============================================================

_engine = None  # stockage global provisoire

def compile_engine(pattern: str) -> None:
    """
    démo : on enregistre juste le motif pour re.search.
    """
    if DEMO:
        _DEMO_STATE["pattern"] = pattern
        return
    raise NotImplementedError("non implémentée")


def matches_line(line: str, ignore_case: bool = False) -> bool:
    """
    Teste si la ligne contient un *suffixe* qui matche (comportement egrep).
    démo : re.search(pattern, line, flags).
    """
    if DEMO:
        pat = _DEMO_STATE.get("pattern")
        if pat is None:
            raise RuntimeError("compile_engine() doit être appelé avant matches_line().")
        flags = re.IGNORECASE if ignore_case else 0
        return re.search(pat, line, flags) is not None
    raise NotImplementedError("non implémenté")


# ============================================================
# I/O utilitaires
# ============================================================

def open_maybe_stdin(path: str, *, encoding: str = "utf-8") -> Iterable[str]:
    if path == "-":
        for line in sys.stdin:
            yield line
    else:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for line in f:
                yield line


def enumerate_lines(lines: Iterable[str]) -> Iterator[Tuple[int, str]]:
    for i, line in enumerate(lines, start=1):
        yield i, line


# ============================================================
# CLI
# ============================================================

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="myegrep",
        description="Clone d’egrep (ERE restreinte).",
        allow_abbrev=False,
    )
    p.add_argument("pattern", help="Expression régulière (ERE restreinte).")
    p.add_argument("file", help="Chemin du fichier texte, ou '-' pour stdin.")
    p.add_argument("-n", "--line-number", action="store_true",
                   help="Afficher le numéro de ligne.")
    p.add_argument("-i", "--ignore-case", action="store_true",
                   help="Ignorer la casse.")
    p.add_argument("--max-matches", type=int, default=0,
                   help="Arrêter après N correspondances (>0).")
    p.add_argument("--dry-run", action="store_true",
                   help="N’affiche que la configuration (pas de match).")
    p.add_argument("--encoding", default="utf-8",
                   help="Encodage du fichier d’entrée (défaut: utf-8).")
    # démo
    p.add_argument("--demo", action="store_true",
                   help="Utiliser un moteur de démonstration basé sur Python 're'.")
    p.add_argument("--version", action="version",
                   version="myegrep 0.1 (DAAR – M2 STL)")
    return p


# ============================================================
# Main
# ============================================================

def main(argv: Optional[list[str]] = None) -> int:
    args_from_sys = sys.argv[1:]

    # mode interactif si aucun argument
    if len(args_from_sys) == 0:
        print("=== Mode interactif de myegrep ===")
        pattern = input("Veuillez entrer le motif à rechercher : ").strip()
        filepath = input("Veuillez indiquer le fichier à analyser : ").strip()
        argv = [pattern, filepath]
    else:
        argv = args_from_sys

    args = build_arg_parser().parse_args(argv)

    # active ou non le mode démo
    global DEMO
    DEMO = bool(args.demo)

    # vérifie d'abord l'existence du fichier (sauf stdin)
    if args.file != "-" and not os.path.exists(args.file):
        sys.stderr.write(f"[ERREUR] Fichier introuvable : {args.file}\n")
        return 2

    # dry-run : affiche la config
    if args.dry_run:
        print(f"[dry-run] pattern={args.pattern!r} file={args.file!r} "
              f"opts(n={args.line_number}, i={args.ignore_case}, "
              f"max={args.max_matches}, enc={args.encoding!r}, demo={DEMO})")
        return 0

    # compilation du motif
    try:
        compile_engine(args.pattern)
    except NotImplementedError as e:
        sys.stderr.write(f"[NYI] {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"[ERREUR] Échec compilation motif : {e}\n")
        return 2

    # lecture & matching
    matches = 0
    try:
        for idx, line in enumerate_lines(open_maybe_stdin(args.file, encoding=args.encoding)):
            try:
                ok = matches_line(line, ignore_case=args.ignore_case)
            except NotImplementedError as e:
                sys.stderr.write(f"[NYI] {e}\n")
                return 2
            except Exception as e:
                sys.stderr.write(f"[ERREUR] Matching échoué : {e}\n")
                return 2

            if ok:
                if args.line_number:
                    sys.stdout.write(f"{idx}:{line}")
                else:
                    sys.stdout.write(line)
                matches += 1
                if args.max_matches and matches >= args.max_matches:
                    break
    except OSError as e:
        sys.stderr.write(f"[ERREUR] Lecture du fichier échouée ({args.file}) : {e}\n")
        return 2

    # codes de sortie egrep : 0 si au moins un match, 1 sinon
    return 0 if matches > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
