# beluga_map

Script Python pour générer une carte interactive des contacts Beluga, facilitant les mises en relation covoiturage.
Le script prend des données de contacts à partir d'un fichier Excel, organise les informations par groupe et génère une carte Folium.
Les marqueurs sur la carte représentent chaque contact avec des icônes colorées en fonction du groupe auquel ils appartiennent.

## Utilisation:
1. Assurez-vous d'avoir les bibliothèques requises installées en exécutant :
   pip install folium pandas

2. Exécutez le script depuis la ligne de commande avec les options suivantes :
  ```
   python script.py --input fichier_contacts.xlsx --output carte_contacts.html
  ```
   Options:
   ```
   --input : Spécifie le fichier Excel contenant les données de contacts (par défaut: exemple_contacts.xlsx).
   --output : Spécifie le nom du fichier HTML de sortie contenant la carte (par défaut: carte_contacts.html).
  ```
3. La carte générée est sauvegardée dans le fichier HTML spécifié et peut être ouverte dans un navigateur web.
   Elle affiche les contacts organisés par groupes avec des informations détaillées dans les popups des marqueurs.

## Note:
- Les adresses sont floutées, et les icônes des marqueurs varient en fonction du groupe et du rôle du parent.
- Les coordonnées doivent être adaptées à chaque lieu de rencontre.
- Les groupes sont organisés en couches pour permettre à l'utilisateur de choisir quels groupes afficher sur la carte.


##  format du fichier excel en entrée
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



