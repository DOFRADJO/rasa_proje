import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List
from difflib import SequenceMatcher
import openai

# Charger le dataset
diseases_df = pd.DataFrame({
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
        "Antiviraux (Oseltamivir 75 mg/jour)", "Consultation médicale"
    ]
})

class ActionDonnerDiagnostic(Action):
    def name(self) -> Text:
        return "action_donner_diagnostic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Récupérer les symptômes de l'utilisateur
        user_symptoms = tracker.latest_message.get('text').lower()

        # Fonction pour calculer la similarité
        def calculate_similarity(symptom_list, user_symptoms):
            matches = [SequenceMatcher(None, symptom.lower(), user_symptoms).ratio() for symptom in symptom_list.split(", ")]
            return sum(matches) / len(matches)

        # Identifier les maladies possibles par similarité
        possible_diseases = []
        for _, row in diseases_df.iterrows():
            similarity = calculate_similarity(row["Symptômes"], user_symptoms)
            if similarity > 0.5:  # Seuil de similarité
                possible_diseases.append(f"{row['Maladie']} (Traitement: {row['Traitement']})")

        # Répondre à l'utilisateur
        if possible_diseases:
            message = f"Les maladies possibles sont : {', '.join(possible_diseases)}."
        else:
            message = "Je n'ai pas pu identifier de maladie correspondant à vos symptômes. Consultez un médecin."

        dispatcher.utter_message(text=message)
        return []

class ActionChatAvecGPT(Action):
    def name(self) -> Text:
        return "action_chat_avec_gpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text')

        # Intégrer GPT pour répondre
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"L'utilisateur a dit : '{user_message}'. Répondez avec une réponse informative.",
            max_tokens=150
        )
        gpt_response = response.choices[0].text.strip()

        dispatcher.utter_message(text=gpt_response)
        return []
