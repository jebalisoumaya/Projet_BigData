# Déploiement avec Docker

Ce projet peut être déployé facilement avec Docker Compose.

## Prérequis

- Docker Desktop installé
- Au moins 8 GB de RAM disponibles pour Docker

## Démarrage

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier les services
docker-compose ps
```

## Services Disponibles

Une fois démarrés, les services sont accessibles via :

- **HDFS NameNode Web UI** : http://localhost:9870
- **YARN ResourceManager** : http://localhost:8088
- **Kafka Broker** : localhost:9092
- **Zookeeper** : localhost:2181

## Utilisation

### Charger des données dans HDFS
```bash
# Copier un fichier dans le conteneur
docker cp hdfs/data/exemple.txt namenode:/tmp/

# Créer les dossiers et charger le fichier
docker exec -it namenode bash
hdfs dfs -mkdir -p /user/data/input
hdfs dfs -put /tmp/exemple.txt /user/data/input/
hdfs dfs -ls /user/data/input
exit
```

### Exécuter un job MapReduce
```bash
# Copier le JAR dans le conteneur
docker cp mapreduce/target/wordcount-1.0.jar resourcemanager:/tmp/

# Exécuter le job
docker exec -it resourcemanager bash
hadoop jar /tmp/wordcount-1.0.jar WordCount /user/data/input /user/data/output
exit

# Voir les résultats
docker exec namenode hdfs dfs -cat /user/data/output/part-r-00000
```

### Utiliser Kafka
```bash
# Créer un topic
docker exec kafka kafka-topics --create \
  --topic evenements \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Lister les topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Producteur et consommateur : utiliser les scripts Python depuis l'hôte
cd kafka/producer
python producer.py

# Dans un autre terminal
cd kafka/consumer
python consumer.py
```

## Arrêt

```bash
# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (ATTENTION: perte de données)
docker-compose down -v
```

## Dépannage

### Vérifier les logs
```bash
docker-compose logs namenode
docker-compose logs kafka
docker-compose logs resourcemanager
```

### Redémarrer un service
```bash
docker-compose restart namenode
```

### État des conteneurs
```bash
docker-compose ps
```
