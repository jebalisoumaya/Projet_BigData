# MapReduce - WordCount

## Description

Ce dossier contient un exemple simple de job MapReduce qui compte les occurrences de chaque mot dans un fichier texte.

## Structure

```
mapreduce/
├── pom.xml                    # Configuration Maven
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── bigdata/
│                   └── WordCount.java    # Code du job MapReduce
└── README.md
```

## Comment ça fonctionne ?

### 1. Mapper (TokenizerMapper)
- Reçoit chaque ligne du fichier d'entrée
- Découpe la ligne en mots
- Nettoie les mots (enlève la ponctuation, met en minuscules)
- Émet pour chaque mot : (mot, 1)

**Exemple :**
```
Entrée : "Bonjour le monde Big Data"
Sortie Mapper :
  (bonjour, 1)
  (le, 1)
  (monde, 1)
  (big, 1)
  (data, 1)
```

### 2. Reducer (IntSumReducer)
- Reçoit un mot et tous ses compteurs
- Additionne tous les compteurs
- Émet : (mot, total)

**Exemple :**
```
Entrée Reducer : (big, [1, 1, 1])
Sortie Reducer : (big, 3)
```

## Compilation

```bash
# Installer les dépendances et compiler
mvn clean package

# Le JAR sera créé dans target/wordcount-1.0.jar
```

## Exécution

### 1. Préparer HDFS
```bash
# Créer les dossiers
hdfs dfs -mkdir -p /user/data/input
hdfs dfs -mkdir -p /user/data/output

# Charger un fichier texte
hdfs dfs -put ../hdfs/data/exemple.txt /user/data/input/
```

### 2. Lancer le job
```bash
hadoop jar target/wordcount-1.0.jar WordCount /user/data/input /user/data/output
```

### 3. Voir les résultats
```bash
# Lister les fichiers de sortie
hdfs dfs -ls /user/data/output

# Afficher les résultats
hdfs dfs -cat /user/data/output/part-r-00000
```

## Résultats attendus

```
apache  1
analyse 1
big     3
data    3
...
```

## Concepts clés

- **Map** : Transformation locale des données
- **Shuffle** : Tri et regroupement par clé (automatique)
- **Reduce** : Agrégation finale
- **Combiner** : Optimisation pour pré-agréger localement

## Exercices pour aller plus loin

1. Modifier le code pour compter uniquement les mots de plus de 5 caractères
2. Trier les résultats par nombre d'occurrences décroissant
3. Créer un nouveau job qui calcule la longueur moyenne des mots
