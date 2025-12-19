#!/usr/bin/env python3
"""
Vérification des transactions et fraudes détectées
"""

import json
from kafka import KafkaConsumer
from collections import Counter

print("=== VERIFICATION DES TRANSACTIONS KAFKA ===\n")

# Créer un consumer
consumer = KafkaConsumer(
    'bank-transactions',
    bootstrap_servers='localhost:9092',
    group_id='verification-group',
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Lire tous les événements
transactions = list(consumer)
consumer.close()

print(f"Total transactions recues: {len(transactions)}\n")

if len(transactions) > 0:
    # Analyse
    types = Counter()
    amounts = []
    frauds = 0
    fraud_amount = 0.0
    
    for msg in transactions:
        data = msg.value
        txn_type = data.get('type', 'Unknown')
        amount = data.get('amount', 0.0)
        
        types[txn_type] += 1
        
        if amount > 0:
            amounts.append(amount)
            
            # Détection fraude (montant > 5000€)
            if amount > 5000:
                frauds += 1
                fraud_amount += amount
                print(f"  FRAUDE: {data.get('user')} - {amount:.2f} EUR - {data.get('item')}")
    
    print(f"\n=== STATISTIQUES ===")
    print(f"Total transactions: {len(transactions)}")
    print(f"Transactions avec montant: {len(amounts)}")
    print(f"Fraudes detectees (>5000 EUR): {frauds}")
    print(f"Montant frauduleux total: {fraud_amount:.2f} EUR")
    
    if amounts:
        print(f"\nMontant moyen: {sum(amounts)/len(amounts):.2f} EUR")
        print(f"Montant max: {max(amounts):.2f} EUR")
        print(f"Montant min: {min(amounts):.2f} EUR")
    
    print(f"\nPar type de transaction:")
    for txn_type, count in types.most_common():
        print(f"  {txn_type}: {count}")
    
    print("\nExemples de transactions:")
    for i, msg in enumerate(transactions[:5]):
        data = msg.value
        print(f"  [{i+1}] {data.get('type')} - {data.get('user')} - {data.get('amount')} EUR")

print("\n=== VERIFICATION TERMINEE ===")
