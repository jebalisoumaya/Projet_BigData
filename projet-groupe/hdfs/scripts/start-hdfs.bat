@echo off
REM Script de démarrage HDFS pour Windows

echo === Demarrage de HDFS ===

REM Vérifier si HADOOP_HOME est défini
if "%HADOOP_HOME%"=="" (
    echo ERREUR: HADOOP_HOME n'est pas defini
    echo Veuillez definir HADOOP_HOME dans vos variables d'environnement
    pause
    exit /b 1
)

REM Formater le NameNode (première utilisation uniquement)
set /p FORMAT="Voulez-vous formater le NameNode? (o/N): "
if /i "%FORMAT%"=="o" (
    echo Formatage du NameNode...
    hdfs namenode -format
)

REM Démarrer HDFS
echo Demarrage du NameNode et des DataNodes...
start "Hadoop NameNode" cmd /k "%HADOOP_HOME%\bin\hdfs.cmd" namenode
timeout /t 3 /nobreak >nul
start "Hadoop DataNode" cmd /k "%HADOOP_HOME%\bin\hdfs.cmd" datanode

REM Attendre que HDFS démarre
timeout /t 10 /nobreak >nul

REM Vérifier l'état
echo === Verification de l'etat HDFS ===
hdfs dfsadmin -report

echo === HDFS demarre avec succes ===
echo Interface Web: http://localhost:9870
pause
