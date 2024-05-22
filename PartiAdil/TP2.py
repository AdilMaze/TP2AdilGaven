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