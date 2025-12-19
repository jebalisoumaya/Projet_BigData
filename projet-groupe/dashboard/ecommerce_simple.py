#!/usr/bin/env python3
"""
Dashboard E-Commerce Simplifié
Lit directement depuis Kafka (pas besoin d'attendre HDFS)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from kafka import KafkaConsumer
import json
from collections import Counter, defaultdict

st.set_page_config(page_title="E-Commerce Analytics", page_icon="🛍️", layout="wide")

# CSS
st.markdown("""
<style>
    .big-metric { font-size: 2rem; font-weight: bold; color: #1f77b4; }
    .success { color: #28a745; }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ E-Commerce Analytics - Temps Réel")
st.markdown("### Données depuis Kafka")

# Bouton pour charger les données
if st.button("🔄 Charger les données depuis Kafka"):
    with st.spinner("Lecture des transactions depuis Kafka..."):
        try:
            # Créer un consumer temporaire
            consumer = KafkaConsumer(
                'bank-transactions',
                bootstrap_servers='localhost:9092',
                auto_offset_reset='earliest',
                consumer_timeout_ms=5000,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            # Lire tous les messages
            stats = {
                'total': 0,
                'connexions': 0,
                'deconnexions': 0,
                'recherches': 0,
                'navigations': 0,
                'ajouts_panier': 0,
                'achats': 0,
                'by_product': Counter(),
                'by_user': defaultdict(list),
                'amounts': []
            }
            
            for message in consumer:
                event = message.value
                stats['total'] += 1
                
                event_type = event.get('type', 'Unknown')
                user = event.get('user', 'Unknown')
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
                
                stats['by_user'][user].append(event_type)
            
            consumer.close()
            
            # Afficher les métriques
            st.success(f"✅ {stats['total']} transactions chargées depuis Kafka")
            
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
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🏆 Top 10 Produits")
                if stats['by_product']:
                    top_products = stats['by_product'].most_common(10)
                    df_products = pd.DataFrame(top_products, columns=['Produit', 'Interactions'])
                    
                    fig = px.bar(df_products, x='Interactions', y='Produit', 
                                orientation='h',
                                color='Interactions',
                                color_continuous_scale='Blues')
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
                st.markdown("**Utilisateurs**")
                st.write(f"Utilisateurs uniques: {len(stats['by_user']):,}")
                if stats['amounts']:
                    st.write(f"Montant max: {max(stats['amounts']):.2f} EUR")
                    st.write(f"Montant min: {min(stats['amounts']):.2f} EUR")
            
            # Tableau des top produits
            if stats['by_product']:
                st.markdown("### 🛒 Tous les Produits")
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

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>🛍️ E-Commerce Analytics - Lecture directe depuis Kafka</div>",
    unsafe_allow_html=True
)
