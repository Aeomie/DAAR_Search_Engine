
# Info
Donc en gros ,  cette version fonctionne et utilise l'approche des états, ce qui n'est pas idéal pour notre cas.
Mais bon, c'est un début, on va essayer de l'améliorer par la suite.

<br>
Ce que j'essaierai de faire maintenant, c'est de développer la version qui utilise un tableau pour faciliter la tâche. 
L'objectif est de faciliter l'accès aux données et de rendre l'ensemble plus convivial et plus optimal.


```bash
# mode classique
python3 main.py "S(a|g|r)+on" test.txt

# mode interactif (aucun argument)
python3 main.py

# mode dry-run (vérifie les options)
python3 main.py --dry-run "S(a|g|r)+on" test.txt

# ignorer la casse
python3 main.py -i "test" test.txt

# numéros de lignes
python3 main.py -n "pattern" file.txt

# démo
python3 main.py --demo "S(a|g|r)+on" test.txt
```
