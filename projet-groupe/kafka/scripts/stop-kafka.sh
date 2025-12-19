#!/bin/bash

# Script d'arrêt Kafka
echo "=== Arrêt de Kafka ==="

if [ -z "$KAFKA_HOME" ]; then
    echo "ERREUR: KAFKA_HOME n'est pas défini"
    exit 1
fi

# Arrêter Kafka
echo "Arrêt du serveur Kafka..."
$KAFKA_HOME/bin/kafka-server-stop.sh

sleep 3

# Arrêter Zookeeper
echo "Arrêt de Zookeeper..."
$KAFKA_HOME/bin/zookeeper-server-stop.sh

echo "=== Kafka arrêté ==="
