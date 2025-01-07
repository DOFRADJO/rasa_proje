# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List  # Importation des types pour annoter les fonctions.
from rasa_sdk import Action, Tracker  # Importation des classes nécessaires pour définir des actions.
from rasa_sdk.executor import CollectingDispatcher  # Utilisé pour envoyer des messages à l'utilisateur.
import pandas as pd  # Bibliothèque pour manipuler le fichier CSV.
import re

'''
# Définition d'une action personnalisée.
class ActionPredictDisease(Action):
    def name(self) -> Text:
        # Nom de l'action, utilisé dans `domain.yml`.
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Fonction principale exécutée par Rasa lorsqu'un utilisateur invoque cette action.

        # Récupération des symptômes saisis par l'utilisateur.
        symptoms = tracker.get_slot("symptoms")

        # Chargement du fichier CSV contenant les maladies et symptômes.
        try:
            data = pd.read_csv("../data/maladies.csv")
            matched_disease = self.match_disease(symptoms, data)
        except Exception as e:
            dispatcher.utter_message(text="Erreur lors du chargement des données.")
            return []

        # Vérification si une maladie correspond aux symptômes saisis.
        if matched_disease:
            dispatcher.utter_message(
                text=f"Sur la base de vos symptômes ({symptoms}), il pourrait s'agir de {matched_disease}. "
                     f"Veuillez consulter un médecin pour confirmation."
            )
        else:
            dispatcher.utter_message(
                text="Je n'ai pas pu identifier de maladie correspondant à vos symptômes. "
                     "Essayez de me donner plus d'informations."
            )
        return []

    @staticmethod
    def match_disease(symptoms: Text, data: pd.DataFrame) -> str:
        # Fonction pour rechercher une correspondance entre les symptômes et une maladie dans le CSV.
        for _, row in data.iterrows():
            csv_symptoms = row["Symptômes"].split(", ")  # Liste des symptômes dans le fichier.
            if all(s in symptoms.lower() for s in csv_symptoms):
                return row["Maladie"]  # Retourne la maladie correspondante si tous les symptômes correspondent.
        return None


class ActionPredictDisease(Action):
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptoms = tracker.get_slot("symptoms")
        dispatcher.utter_message(text=f"{symptoms}")

        # Essayez de lire le fichier CSV et capturer toute exception potentielle.
        data = pd.DataFrame({
    "Maladie": [
        "Anémie", "Cataracte", "Conjonctivite", "Constipation", "Diabète", "Démangeaisons cutanées",
        "Ebola", "Eczéma", "Éjaculation précoce", "Gale", "Grippe", "Kyste au sein",
        "Mauvaise haleine", "Fièvre jaune", "Fièvre typhoïde", "Flatulences", "MST/IST", "Maux de tête",
        "Paludisme", "Panaris", "Dengue", "Migraine", "Mycose de l'ongle", "Mycose de la peau",
        "Mycose génitale", "Myopathie", "Myopie", "Méningite", "Ménopause", "Kyste de l'ovaire",
        "Poliomyélite", "Prostatite", "Rage", "Rougeole", "Sida", "Tuberculose", "Tumeur au cerveau",
        "Tétanos", "Vaginite", "Varicelle", "Variole", "Dartres"
    ],
    "Symptômes": [
        "Fatigue, pâleur, essoufflement", "Vision trouble", "Rougeur, démangeaison des yeux",
        "Douleurs abdominales, ballonnements", "Soif excessive, fatigue", "Rougeur, irritation",
        "Fièvre élevée, saignements", "Plaques rouges, démangeaisons", "Éjaculation rapide",
        "Démangeaisons intenses, lésions cutanées", "Fièvre, maux de gorge", "Masse palpable dans le sein",
        "Mauvaise odeur buccale", "Fièvre, jaunisse", "Fièvre, douleurs abdominales", "Gaz, ballonnements",
        "Écoulements, douleurs", "Douleurs à la tête", "Fièvre, sueurs nocturnes", "Inflammation autour des ongles",
        "Fièvre, douleurs musculaires", "Maux de tête récurrents", "Épaississement des ongles",
        "Plaques rouges, démangeaisons", "Démangeaisons vaginales", "Faiblesse musculaire", "Vision floue",
        "Fièvre, raideur de la nuque", "Bouffées de chaleur", "Douleurs abdominales", "Paralysie",
        "Douleurs urinaires", "Salivation excessive", "Fièvre, éruptions cutanées", "Amaigrissement",
        "Toux persistante", "Toux, douleurs cérébrales", "Spasmes musculaires", "Douleurs vaginales",
        "Fièvre, éruptions", "Pustules", "Plaques sèches"
    ],
    "Traitement": [
        "Suppléments de fer (200 mg/jour, Ferograd ou Tardyferon)", 
        "Chirurgie oculaire, lunettes", 
        "Collyres antibiotiques (Tobramycine 0.3%, 1 goutte 4x/jour)", 
        "Laxatifs (Lactulose 15 ml/jour), hydratation", 
        "Insuline (1-2 unités/kg/jour, Lantus)", 
        "Crèmes apaisantes (Hydrocortisone 1%)", 
        "Soins intensifs", "Crèmes corticoïdes (Betamethasone 0.05%)", 
        "Thérapie comportementale", "Perméthrine topique (5%, application unique)", 
        "Antiviraux (Oseltamivir 75 mg/jour)", "Consultation médicale",
        *["Non spécifié"] * 30  # Remplit avec 'Non spécifié' pour le reste des lignes
    ]
})
        matched_disease = self.match_disease(symptoms, data)
        

        if matched_disease:
            dispatcher.utter_message(
                text=f"Sur la base de vos symptômes ({symptoms}), il pourrait s'agir de {matched_disease['Maladie']}. "
                     f"Traitement proposé: {matched_disease['Traitement']}. "
                     f"Veuillez consulter un médecin pour confirmation."
            )
        else:
            dispatcher.utter_message(
                text="Je n'ai pas pu identifier de maladie correspondant à vos symptômes. "
                     "Essayez de me donner plus d'informations."
            )
        return []

    @staticmethod
    def match_disease(symptoms: Text, data: pd.DataFrame) -> Dict:
        """
        Match symptoms to diseases from a dataframe.
        Returns the first matched disease as a dictionary or None.
        """
        # Nettoyez et normalisez les symptômes donnés (conversion en minuscules, suppression des espaces superflus).
        symptoms = symptoms.lower().strip()

        # Vérifier chaque ligne du fichier CSV.
        for _, row in data.iterrows():
            csv_symptoms = row["Symptômes"].lower().split(", ")  # On suppose que les symptômes dans le fichier sont séparés par des virgules.
            
            # Si tous les symptômes de l'utilisateur sont contenus dans le CSV pour une maladie, on la renvoie.
            if all(symptom in symptoms for symptom in csv_symptoms):
                return row  # Retourne toute la ligne correspondante qui contient 'Maladie', 'Symptômes', etc.

        return None
'''



class ActionPredictDisease(Action):
    def name(self) -> Text:
        # Nom de l'action, utilisé dans `domain.yml`.
        return "action_predict_disease"

    @staticmethod
    def preprocess_symptoms(user_input: Text) -> List[Text]:
        """
        Traite les symptômes saisis par l'utilisateur pour extraire uniquement les mots clés.
        """
        # Supprime "J'ai", les ponctuations, et divise les phrases en morceaux.
        symptoms = re.sub(r"j'ai |j’ai |[^\w\s,]", "", user_input.lower())
        symptoms_list = [s.strip() for s in symptoms.split("et")]  # Divise par "et" pour gérer plusieurs symptômes
        symptoms_list.extend(s.strip() for s in symptoms.split(","))  # Divise par virgule
        return list(set(symptoms_list))  # Évite les doublons

    @staticmethod
    def match_disease(symptoms: List[Text], data: pd.DataFrame) -> str:
        """
        Cherche une correspondance entre les symptômes traités et les données.
        """
        for _, row in data.iterrows():
            csv_symptoms = row["Symptômes"].split(", ")
            if all(s in symptoms for s in csv_symptoms):
                return row["Maladie"]
        return None

    def run(self, dispatcher: CollectingDispatcher, tracker, domain: Dict[Text, Any]) -> list:
        # Symptômes récupérés à partir de l'intent
        user_input = tracker.get_slot("symptoms")
        if not user_input:
            dispatcher.utter_message("Merci de préciser vos symptômes.")
            return []

        # Prétraitement des symptômes utilisateur
        symptoms = self.preprocess_symptoms(user_input)

        # Exemple des données (ajoutez votre DataFrame complet ici)
        data = pd.DataFrame({
    "Maladie": [
        "Anémie", "Cataracte", "Conjonctivite", "Constipation", "Diabète", "Démangeaisons cutanées",
        "Ebola", "Eczéma", "Éjaculation précoce", "Gale", "Grippe", "Kyste au sein",
        "Mauvaise haleine", "Fièvre jaune", "Fièvre typhoïde", "Flatulences", "MST/IST", "Maux de tête",
        "Paludisme", "Panaris", "Dengue", "Migraine", "Mycose de l'ongle", "Mycose de la peau",
        "Mycose génitale", "Myopathie", "Myopie", "Méningite", "Ménopause", "Kyste de l'ovaire",
        "Poliomyélite", "Prostatite", "Rage", "Rougeole", "Sida", "Tuberculose", "Tumeur au cerveau",
        "Tétanos", "Vaginite", "Varicelle", "Variole", "Dartres"
    ],
    "Symptômes": [
        "Fatigue, pâleur, essoufflement", "Vision trouble", "Rougeur, démangeaison des yeux",
        "Douleurs abdominales, ballonnements", "Soif excessive, fatigue", "Rougeur, irritation",
        "Fièvre élevée, saignements", "Plaques rouges, démangeaisons", "Éjaculation rapide",
        "Démangeaisons intenses, lésions cutanées", "Fièvre, maux de gorge", "Masse palpable dans le sein",
        "Mauvaise odeur buccale", "Fièvre, jaunisse", "Fièvre, douleurs abdominales", "Gaz, ballonnements",
        "Écoulements, douleurs", "Douleurs à la tête", "Fièvre, sueurs nocturnes", "Inflammation autour des ongles",
        "Fièvre, douleurs musculaires", "Maux de tête récurrents", "Épaississement des ongles",
        "Plaques rouges, démangeaisons", "Démangeaisons vaginales", "Faiblesse musculaire", "Vision floue",
        "Fièvre, raideur de la nuque", "Bouffées de chaleur", "Douleurs abdominales", "Paralysie",
        "Douleurs urinaires", "Salivation excessive", "Fièvre, éruptions cutanées", "Amaigrissement",
        "Toux persistante", "Toux, douleurs cérébrales", "Spasmes musculaires", "Douleurs vaginales",
        "Fièvre, éruptions", "Pustules", "Plaques sèches"
    ],
    "Traitement": [
        "Suppléments de fer (200 mg/jour, Ferograd ou Tardyferon)", 
        "Chirurgie oculaire, lunettes", 
        "Collyres antibiotiques (Tobramycine 0.3%, 1 goutte 4x/jour)", 
        "Laxatifs (Lactulose 15 ml/jour), hydratation", 
        "Insuline (1-2 unités/kg/jour, Lantus)", 
        "Crèmes apaisantes (Hydrocortisone 1%)", 
        "Soins intensifs", "Crèmes corticoïdes (Betamethasone 0.05%)", 
        "Thérapie comportementale", "Perméthrine topique (5%, application unique)", 
        "Antiviraux (Oseltamivir 75 mg/jour)", "Consultation médicale",
        *["Non spécifié"] * 30  # Remplit avec 'Non spécifié' pour le reste des lignes
    ]
})

        # Trouver la maladie correspondante
        matched_disease = self.match_disease(symptoms, data)

        # Vérifiez et répondez en conséquence
        if matched_disease:
            dispatcher.utter_message(f"La maladie correspondante est : {matched_disease}")
        else:
            dispatcher.utter_message("Aucune correspondance trouvée pour vos symptômes.")

        return []
