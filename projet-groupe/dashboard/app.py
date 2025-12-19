#!/usr/bin/env python3
"""
DASHBOARD BIG DATA - Architectu# Sid# Sidebar
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Choisir une vue",
    ["📊 Vue d'ensemble", "🗂️ HDFS", "⚙️ MapReduce", "🚀 E-Commerce Analytics"]
)st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Choisir une vue",
    ["📊 Vue d'ensemble", "🗂️ HDFS", "⚙️ MapReduce", "🚀 E-Commerce Analytics", "📡 Kafka & Docker"]
)S + MapReduce + Kafka
Interface de visualisation des résultats
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import (
    get_hdfs_stats,
    get_mapreduce_results,
    get_ecommerce_insights,
    check_kafka_status,
    get_docker_services
)

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Big Data",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .status-running {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Choisir une vue",
    ["📊 Vue d'ensemble", "🗂️ HDFS", "⚙️ MapReduce", "🚀 E-Commerce Analytics", "�️ E-Commerce Live (Kafka)", "�📡 Kafka & Docker"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Rafraîchissement")
if st.sidebar.button("🔄 Actualiser les données"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Dernière mise à jour:**  \n{datetime.now().strftime('%H:%M:%S')}")

# ==================== PAGE 1: VUE D'ENSEMBLE ====================
if page == "📊 Vue d'ensemble":
    st.markdown('<div class="main-header">🎯 Dashboard Big Data</div>', unsafe_allow_html=True)
    st.markdown("### Architecture HDFS + MapReduce + Kafka")
    
    # Vérifier les services Docker
    services = get_docker_services()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📦 HDFS")
        hdfs_stats = get_hdfs_stats()
        if 'namenode' in services and services['namenode'] == 'running':
            st.markdown(f'<div class="status-running">✓ Actif</div>', unsafe_allow_html=True)
            st.metric("Fichiers", hdfs_stats['total_files'])
            st.metric("Stockage", f"{hdfs_stats['total_size_mb']} MB")
        else:
            st.markdown(f'<div class="status-error">✗ Inactif</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚀 Kafka")
        kafka_status = check_kafka_status()
        if kafka_status['status'] == 'running':
            st.markdown(f'<div class="status-running">✓ Actif</div>', unsafe_allow_html=True)
            st.metric("Topics", kafka_status['topic_count'])
            st.metric("Port", "9092")
        else:
            st.markdown(f'<div class="status-error">✗ Inactif</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### ⚙️ MapReduce")
        if 'resourcemanager' in services and services['resourcemanager'] == 'running':
            st.markdown(f'<div class="status-running">✓ Actif</div>', unsafe_allow_html=True)
            mr_results = get_mapreduce_results()
            st.metric("Mots uniques", f"{mr_results.get('unique_words', 0):,}")
            st.metric("Port YARN", "8088")
        else:
            st.markdown(f'<div class="status-error">✗ Inactif</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistiques E-Commerce
    st.markdown("### 📈 E-Commerce Analytics")
    insights = get_ecommerce_insights()
    
    if insights:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Événements", f"{insights['connexions'] + insights['deconnexions'] + insights['recherches'] + insights['navigations'] + insights['ajouts_panier'] + insights['achats']:,}")
        
        with col2:
            st.metric("Achats", f"{insights['achats']:,}", delta=f"{insights['taux_conversion']:.1f}% conversion")
        
        with col3:
            st.metric("Ajouts Panier", f"{insights['ajouts_panier']:,}")
        
        with col4:
            st.metric("Recherches", f"{insights['recherches']:,}")
        
        # Architecture schema
        st.markdown("---")
        st.markdown("### 🏗️ Architecture du Système")
        
        st.markdown("""
        ```
        ┌─────────────────────────────────────────────────────────────┐
        │                    FLUX DE DONNÉES                          │
        ├─────────────────────────────────────────────────────────────┤
        │                                                             │
        │  📦 HDFS (Stockage)                                         │
        │       ↓                                                     │
        │  🔄 Producer (hdfs_to_kafka.py)                            │
        │       ↓                                                     │
        │  🚀 Kafka (Streaming)                                       │
        │       ↓                                                     │
        │  📊 Consumer + Analyse (ecommerce_analyzer.py)             │
        │       ↓                                                     │
        │  💾 HDFS (Insights persistés)                              │
        │                                                             │
        └─────────────────────────────────────────────────────────────┘
        ```
        """)
    else:
        st.info("ℹ️ Aucune donnée e-commerce disponible. Lancez l'analyse hybride pour voir les résultats.")
    
    # Services Docker
    st.markdown("---")
    st.markdown("### 🐳 Services Docker")
    
    if services:
        df_services = pd.DataFrame([
            {'Service': name, 'Status': '🟢 Running' if status == 'running' else '🔴 Stopped'}
            for name, status in services.items()
        ])
        st.dataframe(df_services, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Impossible de récupérer les services Docker")

# ==================== PAGE 2: HDFS ====================
elif page == "🗂️ HDFS":
    st.markdown('<div class="main-header">📦 HDFS - Stockage Distribué</div>', unsafe_allow_html=True)
    
    hdfs_stats = get_hdfs_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Nombre de fichiers", hdfs_stats['total_files'], delta=None)
    
    with col2:
        st.metric("Stockage total", f"{hdfs_stats['total_size_mb']} MB", delta=None)
    
    st.markdown("---")
    st.markdown("### 📂 Fichiers stockés")
    
    if hdfs_stats['files']:
        df_files = pd.DataFrame(hdfs_stats['files'])
        df_files['size_mb'] = df_files['size'].apply(lambda x: round(x / (1024*1024), 2))
        
        # Graphique des tailles de fichiers
        fig = px.bar(df_files, x='name', y='size_mb', 
                     title="Taille des fichiers (MB)",
                     labels={'name': 'Fichier', 'size_mb': 'Taille (MB)'},
                     color='size_mb',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé
        st.dataframe(df_files[['name', 'size_mb']], use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Aucun fichier trouvé dans HDFS")
    
    st.markdown("---")
    st.markdown("### 🔗 Accès Web HDFS")
    st.markdown("🌐 [Ouvrir HDFS Web UI](http://localhost:9870)")

# ==================== PAGE 3: MAPREDUCE ====================
elif page == "⚙️ MapReduce":
    st.markdown('<div class="main-header">⚙️ MapReduce - WordCount</div>', unsafe_allow_html=True)
    
    mr_results = get_mapreduce_results()
    
    if mr_results['success']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Mots uniques", f"{mr_results['unique_words']:,}")
        
        with col2:
            st.metric("Total de mots", f"{mr_results['total_words']:,}")
        
        st.markdown("---")
        st.markdown("### 🏆 Top 10 des mots les plus fréquents")
        
        if mr_results['top_words']:
            df_words = pd.DataFrame(mr_results['top_words'], columns=['Mot', 'Fréquence'])
            
            # Graphique horizontal
            fig = px.bar(df_words, x='Fréquence', y='Mot', orientation='h',
                         title="Mots les plus fréquents",
                         color='Fréquence',
                         color_continuous_scale='Viridis')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau
            st.dataframe(df_words, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Aucun résultat disponible")
    else:
        st.error("❌ Impossible de récupérer les résultats MapReduce")
    
    st.markdown("---")
    st.markdown("### 🔗 Interfaces Web")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🌐 [YARN ResourceManager](http://localhost:8088)")
    with col2:
        st.markdown("🌐 [History Server](http://localhost:8188)")

# ==================== PAGE 4: E-COMMERCE ====================
elif page == "🚀 E-Commerce Analytics":
    st.markdown('<div class="main-header">📊 E-Commerce Analytics - Lecture Kafka</div>', unsafe_allow_html=True)
    st.markdown("### Données en temps réel depuis Kafka")
    
    # Bouton pour charger depuis Kafka
    if st.button("🔄 CHARGER LES DONNÉES DEPUIS KAFKA", type="primary", use_container_width=True):
        with st.spinner("📡 Lecture de TOUTES les transactions depuis Kafka..."):
            try:
                from kafka import KafkaConsumer
                import json
                from collections import Counter, defaultdict
                
                consumer = KafkaConsumer(
                    'bank-transactions',
                    bootstrap_servers='localhost:9092',
                    auto_offset_reset='earliest',
                    consumer_timeout_ms=10000,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                )
                
                stats = {
                    'total': 0,
                    'connexions': 0,
                    'deconnexions': 0,
                    'recherches': 0,
                    'navigations': 0,
                    'ajouts_panier': 0,
                    'achats': 0,
                    'by_product': Counter(),
                    'amounts': []
                }
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                message_count = 0
                for message in consumer:
                    event = message.value
                    stats['total'] += 1
                    message_count += 1
                    
                    if message_count % 1000 == 0:
                        progress_bar.progress(min(message_count / 100000, 1.0))
                        status_text.text(f"Traitement: {message_count:,} messages...")
                    
                    event_type = event.get('type', 'Unknown')
                    item = event.get('item', '')
                    amount = event.get('amount', 0)
                    
                    if event_type == 'CONNEXION':
                        stats['connexions'] += 1
                    elif event_type == 'DECONNEXION':
                        stats['deconnexions'] += 1
                    elif event_type == 'RECHERCHE':
                        stats['recherches'] += 1
                        if item:
                            stats['by_product'][item] += 1
                    elif event_type == 'NAVIGATION':
                        stats['navigations'] += 1
                    elif event_type == 'AJOUT_PANIER':
                        stats['ajouts_panier'] += 1
                    elif event_type == 'ACHAT':
                        stats['achats'] += 1
                        if amount > 0:
                            stats['amounts'].append(amount)
                        if item:
                            stats['by_product'][item] += 1
                
                consumer.close()
                progress_bar.progress(1.0)
                status_text.empty()
                
                st.success(f"✅ {stats['total']:,} transactions chargées depuis Kafka")
                
                # Métriques principales
                st.markdown("### 📈 Métriques Clés")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Événements", f"{stats['total']:,}")
                
                with col2:
                    st.metric("Achats", f"{stats['achats']:,}")
                
                with col3:
                    if stats['ajouts_panier'] > 0:
                        taux = (stats['achats'] / stats['ajouts_panier']) * 100
                        st.metric("Taux Conversion", f"{taux:.1f}%")
                    else:
                        st.metric("Taux Conversion", "N/A")
                
                with col4:
                    if stats['amounts']:
                        avg = sum(stats['amounts']) / len(stats['amounts'])
                        st.metric("Montant Moyen", f"{avg:.2f} EUR")
                    else:
                        st.metric("Montant Moyen", "N/A")
                
                st.markdown("---")
                
                # Graphiques
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Distribution des Événements")
                    event_data = pd.DataFrame([
                        {'Type': 'Connexions', 'Count': stats['connexions']},
                        {'Type': 'Déconnexions', 'Count': stats['deconnexions']},
                        {'Type': 'Recherches', 'Count': stats['recherches']},
                        {'Type': 'Navigations', 'Count': stats['navigations']},
                        {'Type': 'Ajouts Panier', 'Count': stats['ajouts_panier']},
                        {'Type': 'Achats', 'Count': stats['achats']}
                    ])
                    
                    fig = px.bar(event_data, x='Type', y='Count', 
                                color='Count',
                                color_continuous_scale='Viridis',
                                title="Types d'événements")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### 🏆 Top 10 Produits")
                    if stats['by_product']:
                        top_products = stats['by_product'].most_common(10)
                        df_products = pd.DataFrame(top_products, columns=['Produit', 'Interactions'])
                        
                        fig = px.bar(df_products, x='Interactions', y='Produit', 
                                    orientation='h',
                                    color='Interactions',
                                    color_continuous_scale='Blues',
                                    title="Produits populaires")
                        fig.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Aucun produit trouvé")
                
                st.markdown("---")
                
                # Statistiques détaillées
                st.markdown("### 📈 Statistiques Détaillées")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Événements par type**")
                    st.write(f"Connexions: {stats['connexions']:,}")
                    st.write(f"Déconnexions: {stats['deconnexions']:,}")
                    st.write(f"Recherches: {stats['recherches']:,}")
                
                with col2:
                    st.write(f"Navigations: {stats['navigations']:,}")
                    st.write(f"Ajouts Panier: {stats['ajouts_panier']:,}")
                    st.write(f"Achats: {stats['achats']:,}")
                
                with col3:
                    st.markdown("**Montants**")
                    if stats['amounts']:
                        st.write(f"Montant max: {max(stats['amounts']):.2f} EUR")
                        st.write(f"Montant min: {min(stats['amounts']):.2f} EUR")
                        st.write(f"Montant total: {sum(stats['amounts']):,.2f} EUR")
                
                # Tableau des top produits
                if stats['by_product']:
                    st.markdown("### 🛒 Top 20 Produits - Tableau Détaillé")
                    all_products = pd.DataFrame(
                        stats['by_product'].most_common(20),
                        columns=['Produit', 'Interactions']
                    )
                    st.dataframe(all_products, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture de Kafka: {str(e)}")
                st.info("💡 Assurez-vous que Kafka est démarré et que des données ont été envoyées.")
    
    else:
        st.info("👆 Cliquez sur le bouton ci-dessus pour charger les données depuis Kafka")
        
        st.markdown("### 📋 Informations")
        st.markdown("""
        Ce dashboard lit les transactions **directement depuis Kafka** (topic: `bank-transactions`).
        
        **Pour générer des données :**
        ```bash
        python hybride/hdfs_to_kafka.py
        ```
        
        **Configuration :**
        - Kafka Broker: `localhost:9092`
        - Topic: `bank-transactions`
        - Mode: Lecture complète depuis le début
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🎯 Dashboard Big Data - Architecture HDFS + MapReduce + Kafka | "
    f"Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)
