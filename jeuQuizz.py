# §§§ VOICI LE QUIZZ DE GWILLYANN !!! §§§
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:01:22 2023

"""

import json
import random

def charger_configuration():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def afficher_menu_quiz(config):
    print("\n=== Choisissez votre quiz ===")
    for i, quiz in enumerate(config['quiz_disponibles'], 1):
        print(f"{i}. {quiz['nom']}")
    print("0. Quitter le jeu")
    
    while True:
        try:
            choix = int(input("\nVotre choix : "))
            if 0 <= choix <= len(config['quiz_disponibles']):
                return choix - 1 if choix > 0 else None
            print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

def choisir_nombre_questions():
    print("\nCombien de questions souhaitez-vous ? (entre 1 et 10)")
    while True:
        try:
            nb_questions = int(input("Votre choix : "))
            if 1 <= nb_questions <= 10:
                return nb_questions
            print("Veuillez entrer un nombre entre 1 et 10.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def selectionner_questions(quiz, nb_questions_demandees):
    toutes_questions = quiz['questions']
    nombre_questions = min(nb_questions_demandees, len(toutes_questions))
    return random.sample(toutes_questions, nombre_questions)

def generer_choix_reponses(question):
    """Génère les choix de réponses pour une question donnée."""
    # On s'assure que toutes les bonnes réponses sont incluses
    reponses_possibles = [r for r in question['reponses_possibles'] 
                         if r not in question['reponses_correctes']]
    nombre_choix = min(question['nombre_choix'], len(question['reponses_possibles']))
    
    # Calculer combien de mauvaises réponses on peut ajouter
    nb_bonnes_reponses = len(question['reponses_correctes'])
    nb_mauvaises_reponses = nombre_choix - nb_bonnes_reponses
    
    # Sélectionner les mauvaises réponses aléatoirement
    mauvaises_reponses = random.sample(reponses_possibles, nb_mauvaises_reponses)
    
    # Combiner avec les bonnes réponses et mélanger
    choix = mauvaises_reponses + question['reponses_correctes']
    random.shuffle(choix)
    
    return choix

def afficher_question(question, numero):
    print(f"\nQuestion {numero}:")
    print(question['question'])
    print("\nTapez 'exit' pour retourner à l'accueil")
    
    # Générer et stocker les choix pour cette question
    choix_reponses = generer_choix_reponses(question)
    question['reponses'] = choix_reponses
    
    for i, reponse in enumerate(choix_reponses, 1):
        print(f"{i}. {reponse}")
    
    if question['type'] == 'multiple':
        print("\nPlusieurs réponses sont possibles. Entrez les numéros séparés par des espaces.")
    
    while True:
        try:
            reponse_str = input("\nVotre réponse (entrez le(s) numéro(s)): ").lower()
            if reponse_str == 'exit':
                return 'exit'
            if question['type'] == 'simple':
                reponse = int(reponse_str)
                if 1 <= reponse <= len(choix_reponses):
                    return [reponse]
            else:  # type multiple
                reponses = [int(r) for r in reponse_str.split()]
                if all(1 <= r <= len(choix_reponses) for r in reponses):
                    return reponses
            print("Veuillez entrer un/des numéro(s) valide(s).")
        except ValueError:
            print("Format invalide. Veuillez réessayer.")

def evaluer_reponse(question, numeros_reponses): # On evaluer la reponse
    reponses_donnees = {question['reponses'][i-1] for i in numeros_reponses} # On recupere les reponses donnees
    reponses_correctes = set(question['reponses_correctes']) # On recupere les reponses correctes
    
    if reponses_donnees == reponses_correctes: # Si les reponses donnees sont egales aux reponses correctes
        print("Bravo ! C'est la bonne réponse !") # On affiche que c'est la bonne reponse
        return 1 # On retourne 1    
    else:
        print("Désolé, la/les bonne(s) réponse(s) était/étaient :", # On affiche les reponses correctes
              ", ".join(question['reponses_correctes']))
        return 0

def jouer_quiz(quiz, nom_joueur): # On joue le quiz
    print(f"\n=== Quiz : {quiz['nom']} ===")
    nb_questions = choisir_nombre_questions() # On choisit le nombre de questions
    questions_selectionnees = selectionner_questions(quiz, nb_questions) # On selectionne les questions
    
    score = 0
    total_questions = len(questions_selectionnees)
    
    for i, question in enumerate(questions_selectionnees, 1):
        reponses = afficher_question(question, i)
        if reponses == 'exit':
            return 2  # Retour au menu principal
        score += evaluer_reponse(question, reponses)
        
    print(f"\nQuiz terminé, {nom_joueur}!") # Le quizz est terminé, on affiche le nom du joueur
    print(f"Votre score: {score}/{total_questions}") # On affiche le score
    
    print("\nQue souhaitez-vous faire ?") # On affiche les options
    print("1. Rejouer ce quiz")
    print("2. Choisir un autre quiz")
    print("3. Quitter")
    
    while True:
        try:
            choix = int(input("\nVotre choix : ")) # On demande au joueur de choisir une option
            if 1 <= choix <= 3:
                return choix
            print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

def main():
    config = charger_configuration()
    print("*** Bienvenue dans le Quiz ! ***\n")
    nom = input("Entrez votre nom: ").title() # On demande le nom du joueur
    print(f"Bonjour et bienvenue {nom} !")
    
    quiz_actuel = None # On initialise le quiz actuel
    while True:
        if quiz_actuel is None:
            choix_quiz = afficher_menu_quiz(config)
            if choix_quiz is None:
                print("\nMerci d'avoir joué ! À bientôt !")
                break
            quiz_actuel = config['quiz_disponibles'][choix_quiz]
        
        choix_fin = jouer_quiz(quiz_actuel, nom)
        
        if choix_fin == 1:  # Rejouer le même quiz
            continue
        elif choix_fin == 2:  # Choisir un autre quiz
            quiz_actuel = None
        else:  # Quitter
            print("\nMerci d'avoir joué ! À bientôt !")
            break

if __name__ == "__main__":
    main()