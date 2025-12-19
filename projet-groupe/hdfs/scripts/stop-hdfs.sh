#!/bin/bash

# Script d'arrêt HDFS
echo "=== Arrêt de HDFS ==="

# Vérifier si HADOOP_HOME est défini
if [ -z "$HADOOP_HOME" ]; then
    echo "ERREUR: HADOOP_HOME n'est pas défini"
    exit 1
fi

# Arrêter HDFS
$HADOOP_HOME/sbin/stop-dfs.sh

echo "=== HDFS arrêté ==="
