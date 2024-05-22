'''
Code pour calculer les données CSV Altitude avec un Menu
@auteur(e)s     X.Adil X.Maziz et Y.Gaven Y.D'Haiti
@matricules     e2388395 et e2280278
@date              20-05-2024
            '''


import csv
import json
import math

class DonneesGeo:
    def __init__(self, ville, pays, latitude, longitude):
        self.ville = ville
        self.pays = pays
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f'{self.ville}, {self.pays}, {self.latitude}, {self.longitude}'

def lireDonneesCsv(fichier_csv):
    liste_donnees = []
    try:
        with open(fichier_csv, mode='r', newline='', encoding='utf-8') as fichier:
            lecteur_csv = csv.DictReader(fichier)
            # Sassurez que les noms de champs n'ont pas d'espaces de début/fin.
            lecteur_csv.fieldnames = [field.strip() for field in lecteur_csv.fieldnames]
            for ligne in lecteur_csv:
                donnee = DonneesGeo(
                    ligne['Ville'].strip(),
                    ligne['Pays'].strip(),
                    ligne['Latitude'].strip().replace(' ', ''),
                    ligne['Longitude'].strip().replace(' ', '')
                )

                liste_donnees.append(donnee)
    except Exception as e:
        print(f"Erreur: {e}")
    return liste_donnees

def ecrireDonneesJson(nomFichier, listeObjDonneesGeo):
    try:
        liste_dict = [donnee.__dict__ for donnee in listeObjDonneesGeo]
        with open(nomFichier, mode='w', encoding='utf-8') as fichier:
            json.dump(liste_dict, fichier, ensure_ascii=False, indent=4)
        print(f"Les données ont été sauvegardées dans {nomFichier}.")
    except Exception as e:
        print(f"Erreur: {e}")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Rayon de la Terre en kilomètres
    phi1 = math.radians(lat1)  # Conversion de la latitude du premier point en radians
    phi2 = math.radians(lat2)  # Conversion de la latitude du deuxième point en radians
    delta_phi = math.radians(lat2 - lat1)  # Différence de latitude en radians
    delta_lambda = math.radians(lon2 - lon1)  # Différence de longitude en radians

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Retourne la distance en kilomètres

def trouverDistanceMin(fichier_json):
    try:
        # Ouverture du fichier JSON en mode lecture
        with open(fichier_json, mode='r', encoding='utf-8') as fichier:
            # Chargement des donnés JSON dans une liste de dictionnaires
            donnees = json.load(fichier)
            # Création des objet DonneesGeo a partir des dictionnaires
            objets_geo = [DonneesGeo(**donnee) for donnee in donnees]

        # Initialisation de la distance minimale a une valeur infinie
        min_distance = float('inf')
        # Initialisation des villes associées a la distance minimale
        ville1, ville2 = None, None

        # Parcours de toutes les paires de villes pour trouver la distance minimale
        for i in range(len(objets_geo)):
            for j in range(i + 1, len(objets_geo)):
                # Calcul de la distance entre les deux villes
                dist = haversine(objets_geo[i].latitude, objets_geo[i].longitude, objets_geo[j].latitude, objets_geo[j].longitude)
                # Mise à jour de la distance minimale et des villes associées si une nouvelle distance minimale est trouvée
                if dist < min_distance:
                    min_distance = dist
                    ville1, ville2 = objets_geo[i], objets_geo[j]

        # Affichage des résultats si des villes ont été trouvées
        if ville1 and ville2:
            print(f"Distance minimale en kilomètres entre 2 villes : {ville1.ville}, {ville1.pays} <{ville1.latitude}°N, {ville1.longitude}°E> et {ville2.ville}, {ville2.pays} <{ville2.latitude}°N, {ville2.longitude}°E> Distance en kilomètres : {min_distance}")
            # Sauvegarde des distances dans un fichier CSV
            sauvegarderDistanceCsv('distances.csv', ville1, ville2, min_distance)
    except Exception as e:
        # Gestion des erreurs en affichant un message
        print(f"Erreur: {e}")


def sauvegarderDistanceCsv(nomFichier, ville1, ville2, distance):
    try:
        # Ouverture du fichier CSV en mode écriture
        with open(nomFichier, mode='w', newline='', encoding='utf-8') as fichier:
            # Création d'un objet writer pour écrire dans le fichier CSV
            writer = csv.writer(fichier)
            # Écriture de l'en-tête des colonnes dans le fichier CSV
            writer.writerow(['Ville1', 'Pays1', 'Latitude1', 'Longitude1', 'Ville2', 'Pays2', 'Latitude2', 'Longitude2', 'Distance'])
            # Écriture des données des deux villes et de la distance dans le fichier CSV
            writer.writerow([ville1.ville, ville1.pays, ville1.latitude, ville1.longitude, ville2.ville, ville2.pays, ville2.latitude, ville2.longitude, distance])
        # Affichage d'un message de confirmation de la sauvegarde
        print(f"Les distances ont été sauvegardées dans {nomFichier}.")
    except Exception as e:
        # Gestion des erreurs en affichant un message
        print(f"Erreur: {e}")


def menu():
    choix_menu = {
        '1': lire_afficher_csv,
        '2': sauvegarder_json,
        '3': calculer_afficher_distance_min,
        'q': quitter
    }

    while True:
        print("\nMenu :")
        print("1- Lire les données du fichier csv, créer les objets et afficher les données.")
        print("2- Sauvegarder les données dans un fichier json.")
        print("3- Lire les données du fichier json, déterminer et afficher les données associées à la distance minimale entre deux villes.")
        print("\nEntrez un numéro pour choisir une option ou appuyez sur 'q' pour quitter :")

        choix = input().strip().lower()
        if choix in choix_menu:
            choix_menu[choix]()
        else:
            print("Choix invalide. Veuillez réessayer.")

def lire_afficher_csv():
    donnees = lireDonneesCsv('C:\\Users\\e2280278\\PycharmProjects\\pythonProject\\Donnees.csv')
    if donnees:
        print("Données du fichier CSV :")
        for donnee in donnees:
            print(donnee)

def sauvegarder_json():
    donnees = lireDonneesCsv('C:\\Users\\e2280278\\PycharmProjects\\pythonProject\\Donnees.csv')
    if donnees:
        ecrireDonneesJson('donnees.json', donnees)

def calculer_afficher_distance_min():
    trouverDistanceMin('donnees.json')

def quitter():
    print("Au revoir!")
    exit()

menu()
