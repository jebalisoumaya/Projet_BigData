#!/usr/bin/env python3
"""
Générateur de données de test pour le projet Big Data

Ce script crée différents types de fichiers de données pour tester 
HDFS et MapReduce avec des volumes plus importants.
"""

import random
import string
from datetime import datetime, timedelta

# Mots pour générer du texte aléatoire
MOTS_BIG_DATA = [
    "big", "data", "hadoop", "mapreduce", "kafka", "hdfs", "streaming",
    "analytics", "processing", "distributed", "cluster", "apache",
    "spark", "hive", "pig", "yarn", "zookeeper", "batch", "real-time",
    "scalable", "parallel", "computation", "storage", "framework"
]

MOTS_FRANCAIS = [
    "bonjour", "projet", "architecture", "traitement", "données",
    "massives", "système", "distribué", "analyse", "fichier",
    "exemple", "test", "université", "cours", "étudiant"
]

PRODUITS = ["laptop", "smartphone", "tablette", "écouteurs", "souris", 
            "clavier", "moniteur", "webcam", "disque-dur", "imprimante"]

PAGES = ["/accueil", "/produits", "/panier", "/compte", "/aide", 
         "/contact", "/recherche", "/categories", "/promotions"]

def generer_texte_simple(nom_fichier, nb_lignes=100000):
    """Génère un fichier texte simple avec des mots aléatoires"""
    print(f"📝 Génération de {nom_fichier} avec {nb_lignes:,} lignes...")
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for i in range(nb_lignes):
            # Mélanger mots français et anglais
            tous_mots = MOTS_BIG_DATA + MOTS_FRANCAIS
            ligne = " ".join(random.choices(tous_mots, k=random.randint(5, 15)))
            f.write(ligne + "\n")
            
            # Afficher la progression
            if (i + 1) % 10000 == 0:
                print(f"  Progression: {i + 1:,} / {nb_lignes:,} lignes")
    
    print(f"✅ {nom_fichier} créé avec succès!\n")

def generer_logs_web(nom_fichier, nb_lignes=50000):
    """Génère des logs d'accès web simulés"""
    print(f"🌐 Génération de {nom_fichier} avec {nb_lignes:,} lignes de logs...")
    
    ips = [f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}" 
           for _ in range(100)]
    
    codes_http = [200, 200, 200, 200, 200, 304, 404, 500, 403]  # 200 plus fréquent
    user_agents = ["Mozilla/5.0", "Chrome/91.0", "Safari/14.0", "Edge/90.0"]
    
    date_debut = datetime.now() - timedelta(days=30)
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for i in range(nb_lignes):
            ip = random.choice(ips)
            date = date_debut + timedelta(seconds=random.randint(0, 30*24*3600))
            page = random.choice(PAGES)
            code = random.choice(codes_http)
            taille = random.randint(500, 50000)
            user_agent = random.choice(user_agents)
            
            log = f'{ip} - - [{date.strftime("%d/%b/%Y:%H:%M:%S +0100")}] "GET {page} HTTP/1.1" {code} {taille} "{user_agent}"'
            f.write(log + "\n")
            
            if (i + 1) % 10000 == 0:
                print(f"  Progression: {i + 1:,} / {nb_lignes:,} lignes")
    
    print(f"✅ {nom_fichier} créé avec succès!\n")

def generer_transactions_ecommerce(nom_fichier, nb_lignes=30000):
    """Génère des transactions e-commerce simulées"""
    print(f"🛒 Génération de {nom_fichier} avec {nb_lignes:,} transactions...")
    
    users = [f"user{i:04d}" for i in range(1, 1001)]
    actions = ["ACHAT", "NAVIGATION", "RECHERCHE", "AJOUT_PANIER", "CONNEXION", "DECONNEXION"]
    
    date_debut = datetime.now() - timedelta(days=30)
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for i in range(nb_lignes):
            date = date_debut + timedelta(seconds=random.randint(0, 30*24*3600))
            user = random.choice(users)
            action = random.choice(actions)
            
            ligne = f"{date.strftime('%Y-%m-%d %H:%M:%S')} {user} {action}"
            
            if action == "ACHAT":
                produit = random.choice(PRODUITS)
                prix = round(random.uniform(10, 1500), 2)
                ligne += f" {produit} {prix}"
            elif action == "NAVIGATION":
                page = random.choice(PAGES)
                ligne += f" {page}"
            elif action == "RECHERCHE":
                terme = random.choice(PRODUITS)
                ligne += f" {terme}"
            elif action == "AJOUT_PANIER":
                produit = random.choice(PRODUITS)
                quantite = random.randint(1, 5)
                ligne += f" {produit} {quantite}"
            
            f.write(ligne + "\n")
            
            if (i + 1) % 10000 == 0:
                print(f"  Progression: {i + 1:,} / {nb_lignes:,} lignes")
    
    print(f"✅ {nom_fichier} créé avec succès!\n")

def generer_livre_fictif(nom_fichier, nb_paragraphes=10000):
    """Génère un 'livre' fictif avec des paragraphes de texte"""
    print(f"📚 Génération de {nom_fichier} avec {nb_paragraphes:,} paragraphes...")
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        for i in range(nb_paragraphes):
            # Générer un paragraphe de 50-200 mots
            nb_mots = random.randint(50, 200)
            paragraphe = " ".join(random.choices(MOTS_FRANCAIS + MOTS_BIG_DATA, k=nb_mots))
            
            # Ajouter ponctuation occasionnelle
            paragraphe = paragraphe.replace(" ", ". ", random.randint(3, 8))
            paragraphe = paragraphe.replace(" ", ", ", random.randint(5, 10))
            paragraphe = paragraphe.capitalize()
            
            f.write(paragraphe + "\n\n")
            
            if (i + 1) % 1000 == 0:
                print(f"  Progression: {i + 1:,} / {nb_paragraphes:,} paragraphes")
    
    print(f"✅ {nom_fichier} créé avec succès!\n")

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🎲 GÉNÉRATEUR DE DONNÉES DE TEST POUR BIG DATA")
    print("="*60 + "\n")
    
    print("Que voulez-vous générer ?")
    print("1. Texte simple (100,000 lignes) - ~5 MB")
    print("2. Logs web (50,000 lignes) - ~8 MB")
    print("3. Transactions e-commerce (30,000 lignes) - ~3 MB")
    print("4. Livre fictif (10,000 paragraphes) - ~15 MB")
    print("5. TOUT générer")
    print("6. Texte TRÈS LARGE (1,000,000 lignes) - ~50 MB")
    
    choix = input("\nVotre choix (1-6) : ").strip()
    
    if choix == "1":
        generer_texte_simple("hdfs/data/texte_large.txt", 100000)
    elif choix == "2":
        generer_logs_web("hdfs/data/logs_web.txt", 50000)
    elif choix == "3":
        generer_transactions_ecommerce("hdfs/data/transactions.txt", 30000)
    elif choix == "4":
        generer_livre_fictif("hdfs/data/livre_fictif.txt", 10000)
    elif choix == "5":
        generer_texte_simple("hdfs/data/texte_large.txt", 100000)
        generer_logs_web("hdfs/data/logs_web.txt", 50000)
        generer_transactions_ecommerce("hdfs/data/transactions.txt", 30000)
        generer_livre_fictif("hdfs/data/livre_fictif.txt", 10000)
    elif choix == "6":
        generer_texte_simple("hdfs/data/texte_tres_large.txt", 1000000)
    else:
        print("❌ Choix invalide!")
        return
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION TERMINÉE !")
    print("="*60)
    print("\nFichiers créés dans le dossier : hdfs/data/")
    print("\nProchaines étapes :")
    print("1. Charger ces fichiers dans HDFS")
    print("2. Lancer un job MapReduce pour les analyser")
    print("\nCommandes :")
    print("  docker cp hdfs/data/texte_large.txt namenode:/tmp/")
    print("  docker exec namenode hdfs dfs -put /tmp/texte_large.txt /user/data/input/")
    print()

if __name__ == "__main__":
    main()
