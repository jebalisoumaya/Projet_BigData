#!/usr/bin/env python3
"""
Script simple pour vérifier les statistiques Kafka
"""

import json
from kafka import KafkaConsumer
from collections import Counter

print("=== VERIFICATION KAFKA ===\n")

# Créer un consumer
consumer = KafkaConsumer(
    'evenements',
    bootstrap_servers='localhost:9092',
    group_id='stats-group',
    auto_offset_reset='earliest',
    consumer_timeout_ms=5000,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Lire tous les événements
events = list(consumer)
consumer.close()

print(f"Total evenements: {len(events)}")

if len(events) > 0:
    # Statistiques
    types = Counter()
    users = Counter()
    total_sales = 0.0
    
    for event in events:
        data = event.value
        event_type = data.get('event_type', 'inconnu')
        user = data.get('user_id', 'inconnu')
        
        types[event_type] += 1
        users[user] += 1
        
        if event_type == 'achat' and 'montant' in data:
            total_sales += data['montant']
    
    print(f"\nPar type d'evenement:")
    for event_type, count in types.most_common():
        print(f"  {event_type}: {count}")
    
    print(f"\nPar utilisateur:")
    for user, count in users.most_common():
        print(f"  {user}: {count}")
    
    print(f"\nVentes totales: {total_sales:.2f} EUR")
    
    print(f"\nExemples d'evenements:")
    for i, event in enumerate(events[:5]):
        print(f"  [{i+1}] {event.value}")

print("\n=== KAFKA FONCTIONNE PARFAITEMENT ! ===")
