# Configuration
pour etre sur que tout fonctionne correctement , il faut éxecuter le makefile , pour installer les libraries malgré que ce sont juste pour les graphes:
```bash
make install
```
# Utilisation du programme

Le programme se lance via Python :

```bash
python engine.py [OPTIONS] pattern fichier
```

### Arguments

- `pattern` : Mot ou motif à rechercher.  
- `fichier` : Chemin vers le fichier texte à analyser. Utilisez `-` pour lire depuis l’entrée standard (stdin).

### Options

- `-h, --help` : Affiche l’aide et quitte le programme.  
- `-m {kmp,boyer,regex}, --mode {kmp,boyer,regex}` : Choisir l’algorithme de recherche (par défaut : regex).  
- `-n, --line-number` : Affiche le numéro de ligne pour chaque correspondance.  
- `-i, --ignore-case` : Ignore la casse lors de la recherche.  
- `--max-matches N` : Arrête après **N** correspondances (>0).  
- `--dry-run` : Affiche uniquement la configuration sans effectuer la recherche.  ( not yet done)
- `--version` : Affiche la version du programme et quitte. ( not yet done)

### Exemples

1. **Recherche simple dans un fichier** :
```bash
python engine.py "motif" fichier.txt
```

**Ignorer la casse et limiter à 10 correspondances** :
```bash
python engine.py -i --max-matches 10 "motif" fichier.txt
```


**Ignorer la casse et limiter à 20 correspondances** :  
Cherche le motif "the" dans le fichier `pg77012.txt` en utilisant l'algorithme KMP, en ignorant la casse et en limitant les résultats à 20 correspondances tout en affichant les numéros de ligne.

```bash
python engine.py -n --max-matches 20 -i -m kmp the pg77012.txt
```


# Utilisation du script `performance.py`

Script de benchmark pour les algorithmes KMP, Boyer–Moore et DFA (regex).

```
usage: pertest [-h] [-f FOLDER] [-m {kmp,boyer,regex}] [-i] [-l | -w] [--max MAX] [--step STEP] pattern
```

## Arguments positionnels
- `pattern` : Motif à chercher.

## Options
- `-h, --help` : Affiche l’aide et quitte.
- `-f FOLDER, --folder FOLDER` : Dossier contenant les fichiers texte à fusionner.
- `-m {kmp,boyer,regex}, --mode {kmp,boyer,regex}` : Choisir le moteur (regex par défaut).
- `-i, --ignore-case` : Ignorer la casse (tout mettre en minuscules).
- `-l, --lines` : Benchmark par lignes (mode par défaut).
- `-w, --words` : Benchmark par mots (active `--step` et `--max`).
- `--max MAX` : Nombre maximal de mots ou lignes à lire.
- `--step STEP` : Nombre de mots ajoutés à chaque itération (uniquement en mode mots).

## Exemple d’utilisation

**Benchmark par lignes en ignorant la casse et en limitant à 100 000 lignes :**

```
python performance.py --ignore-case --max 100000 the
```

**Benchmark par mots dans un dossier spécifique avec Boyer-Moore :**

```
python performance.py -f TestResultsLines -m boyer --words --step 1000 --max 50000 the
```