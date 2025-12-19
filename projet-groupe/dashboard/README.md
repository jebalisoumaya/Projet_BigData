# 🎯 Dashboard Big Data - Streamlit

Interface web de visualisation pour l'architecture HDFS + MapReduce + Kafka.

## 📋 Fonctionnalités

### 5 Pages interactives :

1. **📊 Vue d'ensemble** : État global du système avec tous les services
2. **🗂️ HDFS** : Visualisation des fichiers stockés avec tailles
3. **⚙️ MapReduce** : Résultats WordCount avec top mots
4. **🚀 E-Commerce Analytics** : Patterns détectés, top produits, métriques
5. **📡 Kafka & Docker** : Topics Kafka et statut des conteneurs

## 🚀 Lancement

```powershell
# Dans le répertoire du projet
streamlit run dashboard/app.py
```

Le dashboard sera accessible sur : **http://localhost:8501**

## 📊 Visualisations

- **Métriques en temps réel** : Événements, conversions, montants
- **Graphiques interactifs** : Patterns (camembert), Produits (barres)
- **Tableaux dynamiques** : Fichiers HDFS, Services Docker, Topics Kafka
- **Statuts colorés** : 🟢 Running / 🔴 Stopped

## 🔄 Rafraîchissement

Utilisez le bouton **🔄 Actualiser** dans la sidebar pour recharger les données.

## 📦 Dépendances

- `streamlit` : Framework web
- `plotly` : Graphiques interactifs
- `pandas` : Manipulation de données

## 🎨 Captures d'écran

Le dashboard affiche :
- État des services Docker (Kafka, HDFS, YARN)
- Résultats MapReduce (111,197 mots uniques)
- Analytics e-commerce (2,209 patterns détectés)
- Distribution des événements par type
- Top 10 produits les plus populaires

## 🔗 Liens vers les interfaces natives

- HDFS Web UI : http://localhost:9870
- YARN ResourceManager : http://localhost:8088
- History Server : http://localhost:8188
