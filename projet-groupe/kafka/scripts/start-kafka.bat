@echo off
REM Script de démarrage Kafka pour Windows

echo === Demarrage de Kafka ===

REM Vérifier si KAFKA_HOME est défini
if "%KAFKA_HOME%"=="" (
    echo ERREUR: KAFKA_HOME n'est pas defini
    echo Veuillez definir KAFKA_HOME dans vos variables d'environnement
    pause
    exit /b 1
)

REM Démarrer Zookeeper
echo Demarrage de Zookeeper...
start "Kafka Zookeeper" cmd /k "%KAFKA_HOME%\bin\windows\zookeeper-server-start.bat" "%KAFKA_HOME%\config\zookeeper.properties"

REM Attendre que Zookeeper démarre
echo Attente du demarrage de Zookeeper...
timeout /t 10 /nobreak >nul

REM Démarrer Kafka
echo Demarrage du serveur Kafka...
start "Kafka Server" cmd /k "%KAFKA_HOME%\bin\windows\kafka-server-start.bat" "%KAFKA_HOME%\config\server.properties"

REM Attendre que Kafka démarre
echo Attente du demarrage de Kafka...
timeout /t 10 /nobreak >nul

REM Créer le topic d'exemple
echo Creation du topic 'evenements'...
"%KAFKA_HOME%\bin\windows\kafka-topics.bat" --create --topic evenements --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

REM Vérifier les topics
echo === Liste des topics ===
"%KAFKA_HOME%\bin\windows\kafka-topics.bat" --list --bootstrap-server localhost:9092

echo === Kafka demarre avec succes ===
echo Kafka Broker: localhost:9092
pause
