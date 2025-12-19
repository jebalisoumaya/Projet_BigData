# Kafka - Streaming en Temps Réel

## Description

Ce dossier contient un système de streaming avec Kafka qui simule des événements utilisateurs en temps réel.

## Structure

```
kafka/
├── scripts/
│   ├── start-kafka.sh/.bat    # Démarrage de Kafka et Zookeeper
│   └── stop-kafka.sh           # Arrêt de Kafka
├── producer/
│   └── producer.py             # Générateur d'événements
├── consumer/
│   └── consumer.py             # Traitement des événements
├── requirements.txt            # Dépendances Python
└── README.md
```

## Installation

### 1. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 2. Installer Kafka
- Télécharger depuis https://kafka.apache.org/downloads
- Décompresser et définir `KAFKA_HOME`

## Démarrage

### Windows
```powershell
cd kafka\scripts
.\start-kafka.bat
```

### Linux/Mac
```bash
cd kafka/scripts
./start-kafka.sh
```

## Utilisation

### 1. Lancer le producteur (Génère des événements)
```bash
cd kafka/producer
python producer.py
```

Le producteur génère aléatoirement des événements :
- **connexion** : Un utilisateur se connecte
- **deconnexion** : Un utilisateur se déconnecte
- **achat** : Un utilisateur achète un produit
- **navigation** : Un utilisateur visite une page
- **recherche** : Un utilisateur effectue une recherche

### 2. Lancer le consommateur (Traite les événements)
```bash
cd kafka/consumer
python consumer.py
```

Le consommateur :
- Reçoit les événements en temps réel
- Affiche chaque événement avec des détails
- Calcule des statistiques (nombre d'événements par type, ventes totales, etc.)

## Exemple de Sortie

### Producteur
```
=== Producteur Kafka d'événements ===

✓ Connecté au broker Kafka: localhost:9092
Publication sur le topic: evenements

[1] Événement envoyé: connexion - user3
[2] Événement envoyé: navigation - user1
[3] Événement envoyé: achat - user2
```

### Consommateur
```
=== Consommateur Kafka d'événements ===

✓ Connecté au broker Kafka: localhost:9092
✓ Abonné au topic: evenements

[1] 15:30:45 - CONNEXION
  🔐 Connexion: user3

[2] 15:30:47 - ACHAT
  💰 Achat: laptop - 899.99€

==================================================
📊 STATISTIQUES
==================================================
Total événements: 10
Ventes totales: 1245.50€

Par type d'événement:
  - navigation: 4
  - achat: 3
  - connexion: 2
  - recherche: 1
==================================================
```

## Architecture

```
[Producteur Python]
        ↓
   (événements)
        ↓
[Topic Kafka: evenements]
        ↓
[Consommateur Python]
        ↓
  (statistiques)
```

## Concepts Kafka

### Topic
Un flux de messages organisé par catégorie. Ici : `evenements`

### Producteur
Application qui publie des messages dans un topic

### Consommateur
Application qui lit et traite les messages d'un topic

### Partition
Division d'un topic pour paralléliser le traitement

### Consumer Group
Groupe de consommateurs qui se partagent le travail

## Exercices pour aller plus loin

1. **Ajouter de nouveaux types d'événements**
   - Événement "panier" avec produits
   - Événement "commentaire"

2. **Sauvegarder dans HDFS**
   - Modifier le consommateur pour écrire les événements dans HDFS
   - Analyser ensuite avec MapReduce

3. **Alertes en temps réel**
   - Détecter les achats > 500€
   - Alerter si un utilisateur se connecte 3 fois en 1 minute

4. **Multiple Consommateurs**
   - Un consommateur pour les statistiques
   - Un autre pour sauvegarder dans une base de données

## Commandes Utiles

### Lister les topics
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Voir les messages d'un topic
```bash
kafka-console-consumer.sh --topic evenements --from-beginning --bootstrap-server localhost:9092
```

### Supprimer un topic
```bash
kafka-topics.sh --delete --topic evenements --bootstrap-server localhost:9092
```

## Dépannage

### Le producteur ne peut pas se connecter
- Vérifier que Kafka est démarré
- Vérifier le port 9092

### Les messages ne sont pas reçus
- Vérifier que producteur et consommateur utilisent le même topic
- Redémarrer Kafka et Zookeeper
