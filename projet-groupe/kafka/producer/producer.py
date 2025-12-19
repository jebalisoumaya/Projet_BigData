#!/usr/bin/env python3
"""
Producteur Kafka - Génère des événements utilisateurs simulés
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'evenements'

# Types d'événements possibles
EVENT_TYPES = ['connexion', 'deconnexion', 'achat', 'navigation', 'recherche']

# Utilisateurs simulés
USERS = ['user1', 'user2', 'user3', 'user4', 'user5']

# Pages/Produits
PAGES = ['/accueil', '/produits', '/panier', '/compte', '/aide']
PRODUCTS = ['laptop', 'smartphone', 'tablette', 'ecouteurs', 'souris']

def create_producer():
    """Crée et configure le producteur Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print(f"✓ Connecté au broker Kafka: {KAFKA_BROKER}")
        return producer
    except Exception as e:
        print(f"✗ Erreur de connexion: {e}")
        return None

def generate_event():
    """Génère un événement aléatoire"""
    event_type = random.choice(EVENT_TYPES)
    user = random.choice(USERS)
    
    event = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user,
        'event_type': event_type,
        'session_id': f"session_{random.randint(1000, 9999)}"
    }
    
    # Ajouter des données spécifiques selon le type d'événement
    if event_type == 'navigation':
        event['page'] = random.choice(PAGES)
    elif event_type == 'achat':
        event['product'] = random.choice(PRODUCTS)
        event['price'] = round(random.uniform(10, 1000), 2)
    elif event_type == 'recherche':
        event['query'] = random.choice(PRODUCTS)
    
    return event

def main():
    """Fonction principale"""
    print("=== Producteur Kafka d'événements ===\n")
    
    # Créer le producteur
    producer = create_producer()
    if not producer:
        return
    
    print(f"Publication sur le topic: {TOPIC}")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    try:
        count = 0
        while True:
            # Générer un événement
            event = generate_event()
            
            # Envoyer l'événement
            producer.send(TOPIC, value=event)
            producer.flush()
            
            count += 1
            print(f"[{count}] Événement envoyé: {event['event_type']} - {event['user_id']}")
            
            # Attendre un peu (entre 0.5 et 2 secondes)
            time.sleep(random.uniform(0.5, 2))
            
    except KeyboardInterrupt:
        print(f"\n\n✓ Arrêt du producteur ({count} événements envoyés)")
    finally:
        producer.close()

if __name__ == '__main__':
    main()
