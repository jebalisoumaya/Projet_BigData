#!/bin/bash

# Script de démarrage HDFS
echo "=== Démarrage de HDFS ==="

# Vérifier si HADOOP_HOME est défini
if [ -z "$HADOOP_HOME" ]; then
    echo "ERREUR: HADOOP_HOME n'est pas défini"
    echo "Veuillez définir HADOOP_HOME dans votre .bashrc ou .bash_profile"
    exit 1
fi

# Formater le NameNode (première utilisation uniquement)
read -p "Voulez-vous formater le NameNode? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "Formatage du NameNode..."
    hdfs namenode -format
fi

# Démarrer HDFS
echo "Démarrage du NameNode et des DataNodes..."
$HADOOP_HOME/sbin/start-dfs.sh

# Attendre que HDFS démarre
sleep 5

# Vérifier l'état
echo "=== Vérification de l'état HDFS ==="
hdfs dfsadmin -report

echo "=== HDFS démarré avec succès ==="
echo "Interface Web: http://localhost:9870"
