#!/bin/bash

# Script de démarrage Kafka
echo "=== Démarrage de Kafka ==="

# Vérifier si KAFKA_HOME est défini
if [ -z "$KAFKA_HOME" ]; then
    echo "ERREUR: KAFKA_HOME n'est pas défini"
    echo "Veuillez définir KAFKA_HOME dans votre .bashrc ou .bash_profile"
    exit 1
fi

# Démarrer Zookeeper
echo "Démarrage de Zookeeper..."
$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties

# Attendre que Zookeeper démarre
echo "Attente du démarrage de Zookeeper..."
sleep 5

# Démarrer Kafka
echo "Démarrage du serveur Kafka..."
$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties

# Attendre que Kafka démarre
echo "Attente du démarrage de Kafka..."
sleep 5

# Créer le topic d'exemple
echo "Création du topic 'evenements'..."
$KAFKA_HOME/bin/kafka-topics.sh --create \
    --topic evenements \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 2>/dev/null || echo "Le topic existe déjà"

# Vérifier les topics
echo "=== Liste des topics ==="
$KAFKA_HOME/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

echo "=== Kafka démarré avec succès ==="
echo "Kafka Broker: localhost:9092"
