# beluga_map
generateur de carte pour beluga


##  fichier en entrée
Utilise en input un fichier excel qui contient les colonnes suivante
```
enfant	groupe	parent	contact	lieux de rencontre	adresse 	adresse floute	email
Paul	Louveteau	Louis	06 99 99 99 99	2 rue des lilas montpellier	rue des lilas montpellier	rue des lilas montpellier	tobedone@tobedone.fr
Julie	Louveteau	Anick	06 99 99 99 99	8 rue de la loge montpellier	rue de la loge montpellier	rue de la loge montpellier	tobedone@tobedone.fr
Teji	Eclai.es	Georges	06 99 99 99 99	30 route de nimes Montpellier	route de nimes Montpellier	route de nimes Montpellier	tobedone@tobedone.fr

```


## Execution
```
 python .\generate_beluga_carte.py --help
usage: generate_beluga_carte.py [-h] [--input XLS_INPUT_FILE] [--output HTML_OUTPUT_FILE]

Generateur de la carte des contacts Beluga, pour faciliter les mises en relation covoiturage.

optional arguments:
  -h, --help            show this help message and exit
  --input XLS_INPUT_FILE
                        Nom du fichier contenant les contacts
  --output HTML_OUTPUT_FILE
                        Fichier html de sortie contenant la carte
```

## Exemple
```
python .\generate_beluga_carte.py --input .\exemple_contacts.xlsx --output test.html
generation de la carte a partir du fichier source '.\exemple_contacts.xlsx'
La carte sera générée dans le fichier 'test.html'

Lecture de 3 contacts
- traite  l'adresse 'rue des lilas montpellier'
- traite  l'adresse 'rue de la loge montpellier'
- traite  l'adresse 'route de nimes Montpellier'

Fichier 'test.html' generé.
Terminé

```



