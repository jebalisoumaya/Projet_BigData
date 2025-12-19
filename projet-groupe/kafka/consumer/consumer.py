#!/usr/bin/env python3
"""
Consommateur Kafka - Traite les événements en temps réel
"""

import json
from collections import defaultdict, Counter
from datetime import datetime
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'evenements'
GROUP_ID = 'groupe-consommateur-1'

# Statistiques
stats = {
    'total': 0,
    'by_type': Counter(),
    'by_user': Counter(),
    'total_sales': 0.0
}

def create_consumer():
    """Crée et configure le consommateur Kafka"""
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            group_id=GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',  # Lire uniquement les nouveaux messages
            enable_auto_commit=True
        )
        print(f"✓ Connecté au broker Kafka: {KAFKA_BROKER}")
        print(f"✓ Abonné au topic: {TOPIC}")
        return consumer
    except Exception as e:
        print(f"✗ Erreur de connexion: {e}")
        return None

def process_event(event):
    """Traite un événement et met à jour les statistiques"""
    stats['total'] += 1
    stats['by_type'][event['event_type']] += 1
    stats['by_user'][event['user_id']] += 1
    
    # Traitement spécifique selon le type
    if event['event_type'] == 'achat' and 'price' in event:
        stats['total_sales'] += event['price']
        print(f"  💰 Achat: {event['product']} - {event['price']}€")
    
    elif event['event_type'] == 'connexion':
        print(f"  🔐 Connexion: {event['user_id']}")
    
    elif event['event_type'] == 'navigation':
        print(f"  🌐 Navigation: {event['page']}")
    
    elif event['event_type'] == 'recherche':
        print(f"  🔍 Recherche: {event.get('query', 'N/A')}")

def display_stats():
    """Affiche les statistiques"""
    print("\n" + "="*50)
    print("📊 STATISTIQUES")
    print("="*50)
    print(f"Total événements: {stats['total']}")
    print(f"Ventes totales: {stats['total_sales']:.2f}€")
    print("\nPar type d'événement:")
    for event_type, count in stats['by_type'].most_common():
        print(f"  - {event_type}: {count}")
    print("\nPar utilisateur:")
    for user, count in stats['by_user'].most_common():
        print(f"  - {user}: {count}")
    print("="*50 + "\n")

def main():
    """Fonction principale"""
    print("=== Consommateur Kafka d'événements ===\n")
    
    # Créer le consommateur
    consumer = create_consumer()
    if not consumer:
        return
    
    print("\nEn attente d'événements...")
    print("Appuyez sur Ctrl+C pour afficher les stats et arrêter\n")
    
    try:
        message_count = 0
        for message in consumer:
            event = message.value
            message_count += 1
            
            # Afficher l'événement
            timestamp = datetime.fromisoformat(event['timestamp'])
            print(f"\n[{message_count}] {timestamp.strftime('%H:%M:%S')} - {event['event_type'].upper()}")
            
            # Traiter l'événement
            process_event(event)
            
            # Afficher les stats tous les 10 messages
            if message_count % 10 == 0:
                display_stats()
                
    except KeyboardInterrupt:
        print("\n\nArrêt du consommateur...")
        display_stats()
    finally:
        consumer.close()
        print("✓ Consommateur arrêté")

if __name__ == '__main__':
    main()
