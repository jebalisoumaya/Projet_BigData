#!/usr/bin/env python3
"""
ARCHITECTURE HYBRIDE - Partie 1
Lit les transactions depuis HDFS et les envoie vers Kafka
"""

import json
import time
from kafka import KafkaProducer
from datetime import datetime
import subprocess

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'bank-transactions'
HDFS_FILE = '/user/data/input/transactions.txt'

def create_producer():
    """Crée le producteur Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print(f"✓ Connecté au broker Kafka: {KAFKA_BROKER}")
        return producer
    except Exception as e:
        print(f"✗ Erreur connexion Kafka: {e}")
        return None

def read_from_hdfs():
    """Lit le fichier transactions.txt depuis HDFS"""
    print(f"\n📂 Lecture du fichier HDFS: {HDFS_FILE}")
    
    try:
        # Commande Docker pour lire depuis HDFS
        cmd = f'docker exec namenode hdfs dfs -cat {HDFS_FILE}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ Erreur lecture HDFS: {result.stderr}")
            return []
        
        lines = result.stdout.strip().split('\n')
        print(f"✓ {len(lines)} transactions lues depuis HDFS")
        return lines
    
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return []

def parse_transaction(line):
    """Convertit une ligne en objet transaction JSON"""
    # Format: 2025-11-24 13:36:43 user0471 NAVIGATION /contact
    # ou: 2025-12-11 01:07:14 user0912 ACHAT écouteurs 1219.89
    parts = line.strip().split()
    if len(parts) >= 4:
        # Date et heure
        timestamp = f"{parts[0]} {parts[1]}"
        user = parts[2]
        txn_type = parts[3]
        
        # Pour les achats, il y a un montant
        amount = 0.0
        item = ""
        if txn_type == "ACHAT" and len(parts) >= 6:
            item = parts[4]
            try:
                amount = float(parts[5])
            except:
                amount = 0.0
        elif len(parts) >= 5:
            item = parts[4]
        
        return {
            'transaction_id': f"TXN{hash(line) % 1000000:06d}",
            'timestamp': timestamp,
            'user': user,
            'type': txn_type,
            'item': item,
            'amount': amount,
            'processed_at': datetime.now().isoformat()
        }
    return None

def main():
    """Flux principal: HDFS → Kafka"""
    print("="*60)
    print("🔄 ARCHITECTURE HYBRIDE - HDFS vers Kafka")
    print("="*60)
    
    # 1. Créer le producteur Kafka
    producer = create_producer()
    if not producer:
        return
    
    print(f"✓ Topic Kafka: {TOPIC}")
    
    # 2. Lire les transactions depuis HDFS
    lines = read_from_hdfs()
    if not lines:
        print("✗ Aucune donnée trouvée dans HDFS")
        return
    
    # 3. Envoyer vers Kafka
    print(f"\n📤 Envoi des transactions vers Kafka...")
    sent = 0
    errors = 0
    
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
            
        transaction = parse_transaction(line)
        if transaction:
            try:
                producer.send(TOPIC, transaction)
                sent += 1
                
                # Affichage tous les 100 transactions
                if sent % 100 == 0:
                    print(f"  [{sent}] transactions envoyées...")
                
                # Petit délai pour simuler le temps réel (optionnel)
                time.sleep(0.01)
                
            except Exception as e:
                errors += 1
                print(f"✗ Erreur transaction {i}: {e}")
        else:
            errors += 1
    
    # Flush pour s'assurer que tout est envoyé
    producer.flush()
    producer.close()
    
    # 4. Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"✓ Transactions lues depuis HDFS : {len(lines)}")
    print(f"✓ Transactions envoyées à Kafka : {sent}")
    print(f"✗ Erreurs                        : {errors}")
    print(f"✓ Topic Kafka                    : {TOPIC}")
    print("="*60)
    print("\n✅ Pipeline HDFS → Kafka terminé avec succès !")

if __name__ == "__main__":
    main()
