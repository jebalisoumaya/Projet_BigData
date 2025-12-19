#!/bin/bash

# Script pour initialiser les dossiers HDFS
echo "=== Initialisation des dossiers HDFS ==="

# Créer les dossiers de base
hdfs dfs -mkdir -p /user/data/input
hdfs dfs -mkdir -p /user/data/output
hdfs dfs -mkdir -p /user/logs

# Charger les données d'exemple
echo "Chargement des données d'exemple..."
hdfs dfs -put ../data/exemple.txt /user/data/input/

# Vérifier les dossiers créés
echo "=== Contenu de HDFS ==="
hdfs dfs -ls -R /user

echo "=== Initialisation terminée ==="
