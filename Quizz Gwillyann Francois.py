# On importe les modules nécessaires
# json : pour lire le fichier de configuration
# random : pour mélanger les questions
# time : pour les pauses
# os : pour effacer l'écran
# string : pour les choix multiples
import json
import random
import time
import os
from string import ascii_lowercase

class QuizConfig:
    def __init__(self):
        self.config = self.lire_configuration()
        self.theme_actuel = None
        self.nombre_questions = None
    
    def lire_configuration(self):
        """Lit et retourne la configuration du quiz depuis le fichier JSON"""
        try:
            with open('config.json', 'r', encoding='utf-8') as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            print("❌ Erreur : Le fichier config.json n'a pas été trouvé!")
            exit(1)
        except json.JSONDecodeError:
            print("❌ Erreur : Le fichier config.json est mal formaté!")
            exit(1)
    
    def choisir_theme(self):
        """Permet à l'utilisateur de choisir un thème"""
        print("\nThèmes disponibles :")
        for i, (theme, info) in enumerate(self.config["themes"].items(), 1):
            print(f"{i}. {theme} - {info['description']}")
        
        while True:
            try:
                choix = int(input("\nChoisissez un thème (numéro) : "))
                if 1 <= choix <= len(self.config["themes"]):
                    self.theme_actuel = list(self.config["themes"].keys())[choix - 1]
                    return
                print("❌ Numéro invalide !")
            except ValueError:
                print("❌ Veuillez entrer un numéro valide !")
    
    def choisir_nombre_questions(self):
        """Permet à l'utilisateur de choisir le nombre de questions"""
        theme_info = self.config["themes"][self.theme_actuel]
        nb_questions_defaut = theme_info["nombre_questions_defaut"]
        nb_questions_max = min(len(theme_info["questions"]), 
                             self.config["parametres"]["nombre_questions_max"])
        
        print(f"\nNombre de questions (entre {self.config['parametres']['nombre_questions_min']} "
              f"et {nb_questions_max}, défaut: {nb_questions_defaut}) :")
        
        while True:
            reponse = input("Votre choix (Entrée pour valeur par défaut) : ").strip()
            if reponse == "":
                self.nombre_questions = nb_questions_defaut
                return
            try:
                nombre = int(reponse)
                if self.config["parametres"]["nombre_questions_min"] <= nombre <= nb_questions_max:
                    self.nombre_questions = nombre
                    return
                print("❌ Nombre invalide !")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide !")

def effacer_ecran():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def generer_choix(question_info):
    """Génère les choix pour une question à choix multiples"""
    tous_les_choix = question_info["choix"].copy()
    nombre_choix = min(question_info["nombre_choix"], len(tous_les_choix))
    
    tous_les_choix.remove(question_info["reponse"])
    autres_choix = random.sample(tous_les_choix, nombre_choix - 1)
    
    choix_finaux = autres_choix + [question_info["reponse"]]
    random.shuffle(choix_finaux)
    
    return choix_finaux

def poser_question_choix_multiple(numero, total, question, question_info):
    """Gère une question à choix multiples"""
    print("\n" + "=" * 50)
    print(f"Question {numero}/{total} - {question_info['points']} points")
    print(f"Catégorie : {question_info['categorie']} - Difficulté : {question_info['difficulte']}")
    print("=" * 50)
    print(f"\n{question}")
    
    choix = generer_choix(question_info)
    for i, choix in enumerate(choix):
        print(f"{ascii_lowercase[i]}) {choix}")
    
    while True:
        reponse = input("\nVotre choix (lettre) : ").lower().strip()
        if reponse in ascii_lowercase[:len(choix)]:
            return choix[ord(reponse) - ord('a')]
        print("❌ Réponse invalide ! Veuillez choisir une lettre valide.")

def poser_question_reponse_multiple(numero, total, question, question_info):
    """Gère une question à réponses multiples"""
    print("\n" + "=" * 50)
    print(f"Question {numero}/{total} - {question_info['points']} points")
    print(f"Catégorie : {question_info['categorie']} - Difficulté : {question_info['difficulte']}")
    print("=" * 50)
    print(f"\n{question}")
    print(f"(Donnez {question_info['nombre_reponses_requises']} réponses, séparées par des virgules)")
    
    reponses = input("\nVos réponses : ").strip()
    return [r.strip() for r in reponses.split(",")]

def verifier_reponse_choix_multiple(reponse_joueur, question_info):
    """Vérifie une réponse à choix multiple"""
    reponse_correcte = question_info["reponse"]
    points = question_info["points"]
    
    if reponse_joueur.lower() == reponse_correcte.lower():
        print("\n✨ Bravo ! C'est la bonne réponse ! ✨")
        print(f"➡️ {question_info['explication']}")
        print(f"➡️ Vous gagnez {points} points!")
        return points
    else:
        print(f"\n❌ Dommage... La bonne réponse était : {reponse_correcte}")
        print(f"➡️ {question_info['explication']}")
        return 0

def verifier_reponse_multiple(reponses_joueur, question_info):
    """Vérifie les réponses multiples"""
    reponses_correctes = question_info["reponses"]
    nombre_requis = question_info["nombre_reponses_requises"]
    points = question_info["points"]
    
    # Normalisation des réponses
    reponses_joueur = [r.lower() for r in reponses_joueur]
    reponses_correctes = [r.lower() for r in reponses_correctes]
    
    # Compte les réponses correctes
    bonnes_reponses = [r for r in reponses_joueur if r in reponses_correctes]
    nombre_correct = len(bonnes_reponses)
    
    if nombre_correct == nombre_requis:
        print("\n✨ Parfait ! Toutes vos réponses sont correctes ! ✨")
        print(f"➡️ {question_info['explication']}")
        print(f"➡️ Vous gagnez {points} points!")
        return points
    elif nombre_correct > 0:
        points_partiels = (points * nombre_correct) // nombre_requis
        print(f"\n👍 Vous avez trouvé {nombre_correct}/{nombre_requis} bonnes réponses.")
        print(f"➡️ {question_info['explication']}")
        print(f"➡️ Vous gagnez {points_partiels} points!")
        return points_partiels
    else:
        print("\n❌ Dommage... Voici quelques réponses possibles :")
        print(", ".join(random.sample(question_info["reponses"], min(3, len(question_info["reponses"])))))
        print(f"➡️ {question_info['explication']}")
        return 0

def afficher_resultats(nom_joueur, score, score_max, config):
    """Affiche les résultats du quiz et propose les options de fin"""
    print("\n" + "=" * 50)
    print(f"Quiz terminé, {nom_joueur} !")
    print("=" * 50)
    print(f"\nVotre score : {score}/{score_max} points")
    
    pourcentage = (score / score_max) * 100
    print(f"Soit {pourcentage:.1f}% de réussite")
    
    if pourcentage == 100:
        print("\n🏆 Parfait ! Vous êtes un champion !")
    elif pourcentage >= 75:
        print("\n🌟 Très bien ! Continuez comme ça !")
    elif pourcentage >= 50:
        print("\n👍 Pas mal ! Vous pouvez encore vous améliorer !")
    else:
        print("\n💪 Continuez à pratiquer, vous vous améliorerez !")
    
    print("\nQue souhaitez-vous faire ?")
    print("1. Rejouer le même quiz")
    print("2. Choisir un nouveau quiz")
    print("3. Quitter")
    
    while True:
        choix = input("\nVotre choix (1-3) : ").strip()
        if choix in ["1", "2", "3"]:
            return int(choix)
        print("❌ Choix invalide ! Veuillez choisir 1, 2 ou 3.")

def lancer_quiz(config, nom_joueur, theme=None, nombre_questions=None):
    """Lance une session de quiz avec les paramètres donnés"""
    if theme is None:
        config.choisir_theme()
    if nombre_questions is None:
        config.choisir_nombre_questions()
    
    theme_info = config.config["themes"][config.theme_actuel]
    
    effacer_ecran()
    print(f"\nBonjour {nom_joueur} ! Commençons le quiz !")
    print(f"Thème : {config.theme_actuel}")
    print(f"Nombre de questions : {config.nombre_questions}")
    print("Catégories disponibles : " + ", ".join(theme_info["categories"]))
    
    # Préparation des questions
    questions = list(theme_info["questions"].items())
    questions_melangees = random.sample(questions, config.nombre_questions)
    
    # Initialisation du score
    score = 0
    score_max = sum(q[1]['points'] for q in questions_melangees)
    
    # Boucle des questions
    for numero_question, (question, info) in enumerate(questions_melangees, 1):
        if info["type"] == "choix_multiple":
            reponse = poser_question_choix_multiple(numero_question, config.nombre_questions, 
                                                  question, info)
            score += verifier_reponse_choix_multiple(reponse, info)
        elif info["type"] == "reponse_multiple":
            reponses = poser_question_reponse_multiple(numero_question, config.nombre_questions,
                                                     question, info)
            score += verifier_reponse_multiple(reponses, info)
        
        time.sleep(config.config["parametres"]["temps_pause_entre_questions"])
    
    return score, score_max

def demarrer_quiz():
    """Fonction principale du quiz"""
    effacer_ecran()
    
    # Initialisation de la configuration
    config = QuizConfig()
    
    # Message de bienvenue
    print("*" * 50)
    print("Bienvenue dans le Quiz !")
    print("*" * 50)
    
    # Demande du nom du joueur
    nom_joueur = input("\nComment vous appelez-vous ? : ").strip().title()
    
    while True:
        # Lance une session de quiz
        score, score_max = lancer_quiz(config, nom_joueur)
        
        # Affiche les résultats et obtient le choix de l'utilisateur
        choix = afficher_resultats(nom_joueur, score, score_max, config)
        
        if choix == 1:  # Rejouer le même quiz
            continue
        elif choix == 2:  # Nouveau quiz
            config.theme_actuel = None
            config.nombre_questions = None
        else:  # Quitter
            print("\nMerci d'avoir joué ! À bientôt ! 👋")
            break

# Point d'entrée du programme
if __name__ == "__main__":
    demarrer_quiz()