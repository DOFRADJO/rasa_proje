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
