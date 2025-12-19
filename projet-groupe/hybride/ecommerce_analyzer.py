#!/usr/bin/env python3
"""
ARCHITECTURE HYBRIDE E-COMMERCE
Analyse des patterns d'achat en temps réel
"""

import json
import signal
import sys
from collections import Counter, defaultdict
from datetime import datetime
from kafka import KafkaConsumer
import subprocess
import os

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'bank-transactions'
GROUP_ID = 'ecommerce-analytics-group'
HDFS_INSIGHTS_DIR = '/user/data/ecommerce-insights'
LOCAL_INSIGHTS_FILE = 'ecommerce_insights.txt'

# Statistiques
stats = {
    'total': 0,
    'connexions': 0,
    'deconnexions': 0,
    'recherches': 0,
    'navigations': 0,
    'ajouts_panier': 0,
    'achats': 0,
    'by_product': Counter(),
    'by_user': defaultdict(list)
}

interesting_patterns = []

def signal_handler(sig, frame):
    """Gère l'arrêt avec Ctrl+C"""
    print("\n\nArret de l'analyse...")
    save_to_hdfs()
    display_stats()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def create_consumer():
    """Crée le consommateur Kafka"""
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            group_id=GROUP_ID,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print(f"OK Connecte au broker Kafka: {KAFKA_BROKER}")
        print(f"OK Abonne au topic: {TOPIC}")
        return consumer
    except Exception as e:
        print(f"ERREUR connexion: {e}")
        return None

def analyze_user_journey(user_id):
    """Analyse le parcours d'un utilisateur"""
    journey = stats['by_user'][user_id]
    
    if len(journey) < 2:
        return None
    
    # Pattern: CONNEXION -> RECHERCHE -> AJOUT_PANIER -> ACHAT
    has_connexion = any(e['type'] == 'CONNEXION' for e in journey)
    has_recherche = any(e['type'] == 'RECHERCHE' for e in journey)
    has_ajout = any(e['type'] == 'AJOUT_PANIER' for e in journey)
    has_achat = any(e['type'] == 'ACHAT' for e in journey)
    
    # Parcours d'achat complet
    if has_connexion and has_recherche and has_ajout and has_achat:
        return {
            'pattern': 'PARCOURS_COMPLET',
            'user': user_id,
            'steps': len(journey),
            'description': 'Utilisateur a complete tout le parcours d achat'
        }
    
    # Panier abandonné
    if has_ajout and not has_achat and len(journey) > 3:
        return {
            'pattern': 'PANIER_ABANDONNE',
            'user': user_id,
            'steps': len(journey),
            'description': 'Utilisateur a ajoute au panier mais n a pas achete'
        }
    
    # Chercheur intensif
    recherches = [e for e in journey if e['type'] == 'RECHERCHE']
    if len(recherches) >= 3:
        return {
            'pattern': 'CHERCHEUR_INTENSIF',
            'user': user_id,
            'recherches': len(recherches),
            'description': f'Utilisateur a effectue {len(recherches)} recherches'
        }
    
    return None

def process_event(event):
    """Traite un événement e-commerce"""
    stats['total'] += 1
    
    # Extraire les informations
    user = event.get('user', 'Unknown')
    event_type = event.get('type', 'Unknown')
    item = event.get('item', '')
    amount = event.get('amount', 0)
    
    # Compteurs par type
    if event_type == 'CONNEXION':
        stats['connexions'] += 1
    elif event_type == 'DECONNEXION':
        stats['deconnexions'] += 1
    elif event_type == 'RECHERCHE':
        stats['recherches'] += 1
        if item:
            stats['by_product'][item] += 1
    elif event_type == 'NAVIGATION':
        stats['navigations'] += 1
    elif event_type == 'AJOUT_PANIER':
        stats['ajouts_panier'] += 1
        if item:
            stats['by_product'][f"panier_{item}"] += 1
    elif event_type == 'ACHAT':
        stats['achats'] += 1
        if item:
            stats['by_product'][f"achat_{item}"] += 1
    
    # Enregistrer dans le parcours utilisateur
    stats['by_user'][user].append({
        'type': event_type,
        'item': item,
        'amount': amount,
        'timestamp': event.get('timestamp')
    })
    
    # Analyser le parcours tous les 10 événements de l'utilisateur
    if len(stats['by_user'][user]) % 10 == 0:
        pattern = analyze_user_journey(user)
        if pattern and pattern not in interesting_patterns:
            interesting_patterns.append(pattern)
            print(f">>> PATTERN DETECTE: {pattern['pattern']} - {pattern['user']}")
    
    # Affichage progressif
    if stats['total'] % 1000 == 0:
        print(f"  [{stats['total']}] evenements traites, {len(interesting_patterns)} patterns detectes")

def save_to_hdfs():
    """Sauvegarde les insights dans HDFS"""
    if not interesting_patterns:
        print("\nAucun pattern interessant detecte")
        return
    
    print(f"\nSauvegarde de {len(interesting_patterns)} patterns dans HDFS...")
    
    # 1. Créer le fichier local
    try:
        with open(LOCAL_INSIGHTS_FILE, 'w', encoding='utf-8') as f:
            f.write("# ANALYSE DES PATTERNS E-COMMERCE\n")
            f.write(f"# Generee le: {datetime.now().isoformat()}\n")
            f.write(f"# Total evenements: {stats['total']}\n")
            f.write(f"# Patterns detectes: {len(interesting_patterns)}\n")
            f.write("#" + "="*80 + "\n\n")
            
            # Statistiques générales
            f.write("## STATISTIQUES GENERALES\n")
            f.write(f"Connexions: {stats['connexions']}\n")
            f.write(f"Deconnexions: {stats['deconnexions']}\n")
            f.write(f"Recherches: {stats['recherches']}\n")
            f.write(f"Navigations: {stats['navigations']}\n")
            f.write(f"Ajouts panier: {stats['ajouts_panier']}\n")
            f.write(f"Achats: {stats['achats']}\n")
            f.write(f"Taux conversion: {stats['achats']/stats['ajouts_panier']*100:.1f}%\n" if stats['ajouts_panier'] > 0 else "Taux conversion: N/A\n")
            f.write("\n")
            
            # Top produits
            f.write("## TOP 10 PRODUITS\n")
            for product, count in stats['by_product'].most_common(10):
                f.write(f"{product}: {count}\n")
            f.write("\n")
            
            # Patterns détectés
            f.write("## PATTERNS DETECTES\n")
            for pattern in interesting_patterns:
                f.write(json.dumps(pattern, ensure_ascii=False) + '\n')
        
        print(f"OK Fichier local cree: {LOCAL_INSIGHTS_FILE}")
    except Exception as e:
        print(f"ERREUR creation fichier local: {e}")
        return
    
    # 2. Créer le répertoire dans HDFS
    cmd_mkdir = f'docker exec namenode hdfs dfs -mkdir -p {HDFS_INSIGHTS_DIR}'
    subprocess.run(cmd_mkdir, shell=True, capture_output=True)
    
    # 3. Copier vers HDFS
    insights_file_hdfs = f"{HDFS_INSIGHTS_DIR}/insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    cmd_put = f'docker exec namenode hdfs dfs -put -f {LOCAL_INSIGHTS_FILE} {insights_file_hdfs}'
    
    result = subprocess.run(cmd_put, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"OK Insights sauvegardes dans HDFS: {insights_file_hdfs}")
        os.remove(LOCAL_INSIGHTS_FILE)
    else:
        print(f"ERREUR sauvegarde HDFS: {result.stderr}")

def display_stats():
    """Affiche les statistiques finales"""
    print("\n" + "="*60)
    print("ANALYSE E-COMMERCE - RESULTATS")
    print("="*60)
    print(f"Total evenements        : {stats['total']}")
    print(f"Connexions              : {stats['connexions']}")
    print(f"Deconnexions            : {stats['deconnexions']}")
    print(f"Recherches              : {stats['recherches']}")
    print(f"Navigations             : {stats['navigations']}")
    print(f"Ajouts au panier        : {stats['ajouts_panier']}")
    print(f"Achats                  : {stats['achats']}")
    
    if stats['ajouts_panier'] > 0:
        taux = stats['achats'] / stats['ajouts_panier'] * 100
        print(f"Taux de conversion      : {taux:.1f}%")
    
    print(f"\nUtilisateurs uniques    : {len(stats['by_user'])}")
    print(f"Patterns detectes       : {len(interesting_patterns)}")
    
    print(f"\nTop 5 produits recherches/achetes:")
    for product, count in stats['by_product'].most_common(5):
        print(f"  {product:20} : {count}")
    
    print(f"\nPatterns detectes:")
    pattern_counts = Counter(p['pattern'] for p in interesting_patterns)
    for pattern, count in pattern_counts.items():
        print(f"  {pattern:25} : {count}")
    
    print("="*60)

def main():
    """Flux principal: Kafka → Analyse patterns → HDFS"""
    print("="*60)
    print("ANALYSE E-COMMERCE EN TEMPS REEL")
    print("="*60)
    print(f"Detection de patterns d'achat")
    print(f"Repertoire HDFS: {HDFS_INSIGHTS_DIR}")
    print("\nEn attente d'evenements...")
    print("Appuyez sur Ctrl+C pour arreter et sauvegarder\n")
    
    # Créer le consumer
    consumer = create_consumer()
    if not consumer:
        return
    
    # Traiter les messages
    try:
        for message in consumer:
            event = message.value
            process_event(event)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        consumer.close()
        save_to_hdfs()
        display_stats()
        print("\nSysteme d'analyse arrete")

if __name__ == "__main__":
    main()
