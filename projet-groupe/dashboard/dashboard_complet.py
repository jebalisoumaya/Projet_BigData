#!/usr/bin/env python3
"""
DASHBOARD TOUT-EN-UN - Big Data E-Commerce
Toutes les données sur une seule page !
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from kafka import KafkaConsumer
import json
from collections import Counter, defaultdict
import subprocess

st.set_page_config(page_title="Dashboard Complet", page_icon="🎯", layout="wide")

# CSS
st.markdown("""
<style>
    .big-title { font-size: 3rem; font-weight: bold; text-align: center; color: #1f77b4; }
    .section-title { font-size: 1.8rem; font-weight: bold; color: #2c3e50; margin-top: 2rem; }
    .success { color: #28a745; font-weight: bold; }
    .info-box { background: #e3f2fd; padding: 1rem; border-radius: 5px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎯 Dashboard Big Data Complet</div>', unsafe_allow_html=True)
st.markdown("### Architecture HDFS + MapReduce + Kafka + E-Commerce Analytics")

# Bouton principal pour tout charger
if st.button("🔄 CHARGER TOUTES LES DONNÉES", type="primary", use_container_width=True):
    
    # ==================== SECTION 1: SERVICES DOCKER ====================
    st.markdown('<div class="section-title">🐳 Services Docker</div>', unsafe_allow_html=True)
    
    with st.spinner("Vérification des services..."):
        try:
            cmd = 'docker ps --format "{{.Names}}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            services = [s.strip() for s in result.stdout.split('\n') if s.strip()]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Services actifs", len(services))
            with col2:
                kafka_status = "🟢 Actif" if any('kafka' in s for s in services) else "🔴 Inactif"
                st.metric("Kafka", kafka_status)
            with col3:
                hdfs_status = "🟢 Actif" if any('namenode' in s for s in services) else "🔴 Inactif"
                st.metric("HDFS", hdfs_status)
        except:
            st.warning("Impossible de vérifier les services Docker")
    
    st.markdown("---")
    
    # ==================== SECTION 2: HDFS ====================
    st.markdown('<div class="section-title">📦 HDFS - Stockage</div>', unsafe_allow_html=True)
    
    with st.spinner("Lecture des fichiers HDFS..."):
        try:
            cmd = 'docker exec namenode hdfs dfs -ls /user/data/input'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            files_count = 0
            total_size = 0
            
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('Found'):
                    parts = line.split()
                    if len(parts) >= 8:
                        size = int(parts[4])
                        total_size += size
                        files_count += 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Fichiers HDFS", files_count)
            with col2:
                st.metric("Stockage total", f"{round(total_size / (1024*1024), 2)} MB")
        except:
            st.warning("Impossible de lire HDFS")
    
    st.markdown("---")
    
    # ==================== SECTION 3: MAPREDUCE ====================
    st.markdown('<div class="section-title">⚙️ MapReduce - WordCount</div>', unsafe_allow_html=True)
    
    with st.spinner("Lecture des résultats MapReduce..."):
        try:
            cmd = 'docker exec namenode hdfs dfs -cat /user/data/output/part-r-00000'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n')
            word_counts = {}
            
            for line in lines[:100]:
                if '\t' in line:
                    word, count = line.split('\t')
                    word_counts[word] = int(count)
            
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Mots uniques", f"{len(lines):,}")
            with col2:
                total = sum(word_counts.values())
                st.metric("Total mots", f"{total:,}")
            
            # Graphique top mots
            if top_words:
                df_words = pd.DataFrame(top_words, columns=['Mot', 'Fréquence'])
                fig = px.bar(df_words, x='Fréquence', y='Mot', orientation='h',
                            title="Top 10 Mots", color='Fréquence',
                            color_continuous_scale='Viridis')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Impossible de lire les résultats MapReduce")
    
    st.markdown("---")
    
    # ==================== SECTION 4: KAFKA E-COMMERCE ====================
    st.markdown('<div class="section-title">🛍️ E-Commerce Analytics (Kafka)</div>', unsafe_allow_html=True)
    
    with st.spinner("📡 Lecture de TOUTES les transactions depuis Kafka..."):
        try:
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
            
            for message in consumer:
                event = message.value
                stats['total'] += 1
                
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
            
            st.success(f"✅ {stats['total']:,} transactions chargées depuis Kafka")
            
            # Métriques principales
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
            
            # Graphiques côte à côte
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Distribution des Événements**")
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
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**🏆 Top 10 Produits**")
                if stats['by_product']:
                    top_products = stats['by_product'].most_common(10)
                    df_products = pd.DataFrame(top_products, columns=['Produit', 'Interactions'])
                    
                    fig = px.bar(df_products, x='Interactions', y='Produit', 
                                orientation='h',
                                color='Interactions',
                                color_continuous_scale='Blues')
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques détaillées en colonnes
            st.markdown("**📈 Statistiques Détaillées**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"Connexions: {stats['connexions']:,}")
                st.write(f"Déconnexions: {stats['deconnexions']:,}")
            
            with col2:
                st.write(f"Recherches: {stats['recherches']:,}")
                st.write(f"Navigations: {stats['navigations']:,}")
            
            with col3:
                st.write(f"Ajouts Panier: {stats['ajouts_panier']:,}")
                st.write(f"Achats: {stats['achats']:,}")
            
            # Tableau top produits
            if stats['by_product']:
                st.markdown("**🛒 Top 20 Produits - Tableau Détaillé**")
                all_products = pd.DataFrame(
                    stats['by_product'].most_common(20),
                    columns=['Produit', 'Interactions']
                )
                st.dataframe(all_products, use_container_width=True, hide_index=True)
                
        except Exception as e:
            st.error(f"❌ Erreur Kafka: {str(e)}")
            st.info("💡 Assurez-vous que Kafka est démarré et que des données ont été envoyées.")

else:
    # Affichage initial
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ## 👆 Cliquez sur le bouton ci-dessus pour charger TOUTES les données
    
    ### Ce dashboard affiche :
    - ✅ **Services Docker** : État des conteneurs
    - ✅ **HDFS** : Fichiers et stockage
    - ✅ **MapReduce** : WordCount avec top mots
    - ✅ **Kafka E-Commerce** : Transactions en temps réel avec graphiques
    
    ### Configuration :
    - **Kafka Broker** : `localhost:9092`
    - **Topic** : `bank-transactions`
    - **HDFS** : `/user/data/input` et `/user/data/output`
    
    ### Pour générer des données e-commerce :
    ```bash
    python hybride/hdfs_to_kafka.py
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Liens utiles
    st.markdown("---")
    st.markdown("### 🔗 Liens Utiles")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🌐 [HDFS (9870)](http://localhost:9870)")
    with col2:
        st.markdown("🌐 [YARN (8088)](http://localhost:8088)")
    with col3:
        st.markdown("🌐 [History Server (8188)](http://localhost:8188)")
    with col4:
        st.markdown("📊 [Dashboard](http://localhost:8501)")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🎯 Dashboard Big Data Complet - HDFS + MapReduce + Kafka + E-Commerce"
    "</div>",
    unsafe_allow_html=True
)
