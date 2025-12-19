#!/usr/bin/env python3
"""
Module de chargement des données depuis HDFS et Kafka
pour le dashboard Streamlit
"""

import subprocess
import json
import os
import re
from collections import Counter
from datetime import datetime


def get_hdfs_stats():
    """Récupère les statistiques des fichiers HDFS"""
    try:
        cmd = 'docker exec namenode hdfs dfs -ls /user/data/input'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        files = []
        total_size = 0
        
        for line in result.stdout.split('\n'):
            if line.strip() and not line.startswith('Found'):
                parts = line.split()
                if len(parts) >= 8:
                    size = int(parts[4])
                    name = parts[7].split('/')[-1]
                    files.append({'name': name, 'size': size})
                    total_size += size
        
        return {
            'files': files,
            'total_files': len(files),
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
    except Exception as e:
        return {'files': [], 'total_files': 0, 'total_size_mb': 0, 'error': str(e)}


def get_mapreduce_results():
    """Récupère les résultats du job MapReduce WordCount"""
    try:
        # D'abord essayer de lire depuis le fichier de résultats local
        result_file = os.path.join(os.path.dirname(__file__), '..', 'resultats_wordcount.txt')
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extraire les statistiques principales
                import re
                mots_totaux = re.search(r'Mots totaux\s*:\s*([\d,]+)', content)
                mots_uniques = re.search(r'Mots uniques\s*:\s*([\d,]+)', content)
                
                if mots_totaux and mots_uniques:
                    total_words = int(mots_totaux.group(1).replace(',', ''))
                    unique_words = int(mots_uniques.group(1).replace(',', ''))
                    
                    # Extraire le top 20 des mots
                    lines = content.split('\n')
                    top_words = []
                    in_words_section = False
                    
                    for line in lines:
                        if 'TOUS LES MOTS' in line:
                            in_words_section = True
                            continue
                        
                        if in_words_section and '\t' in line:
                            parts = line.strip().split('\t')
                            if len(parts) == 2 and parts[1].isdigit():
                                word = parts[0]
                                count = int(parts[1])
                                top_words.append((word, count))
                                
                                if len(top_words) >= 20:
                                    break
                    
                    return {
                        'unique_words': unique_words,
                        'total_words': total_words,
                        'top_words': top_words[:20],
                        'success': True
                    }
        
        # Sinon, essayer de lire depuis HDFS
        cmd = 'docker exec namenode hdfs dfs -cat /user/data/output/part-r-00000'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        lines = result.stdout.strip().split('\n')
        
        # Parser les mots et leurs comptages
        word_counts = {}
        total_words = 0
        
        for line in lines[:100]:  # Top 100 mots
            if '\t' in line:
                word, count = line.split('\t')
                word_counts[word] = int(count)
                total_words += int(count)
        
        # Top 20 mots
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return {
            'unique_words': len(lines),
            'total_words': total_words,
            'top_words': top_words,
            'success': True
        }
    except Exception as e:
        return {'unique_words': 0, 'total_words': 0, 'top_words': [], 'success': False, 'error': str(e)}


def get_ecommerce_insights():
    """Récupère les insights e-commerce depuis HDFS"""
    try:
        # Lister les fichiers d'insights
        cmd = 'docker exec namenode hdfs dfs -ls /user/data/ecommerce-insights'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return None
        
        # Trouver le fichier le plus récent
        files = []
        for line in result.stdout.split('\n'):
            if 'insights_' in line:
                files.append(line.split()[-1])
        
        if not files:
            return None
        
        latest_file = sorted(files)[-1]
        
        # Lire le contenu
        cmd = f'docker exec namenode hdfs dfs -cat {latest_file}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parser les statistiques
        content = result.stdout
        stats = {
            'connexions': 0,
            'deconnexions': 0,
            'recherches': 0,
            'navigations': 0,
            'ajouts_panier': 0,
            'achats': 0,
            'taux_conversion': 0,
            'patterns': {'PARCOURS_COMPLET': 0, 'PANIER_ABANDONNE': 0, 'CHERCHEUR_INTENSIF': 0},
            'top_products': []
        }
        
        lines = content.split('\n')
        in_stats = False
        in_products = False
        in_patterns = False
        
        for line in lines:
            if '## STATISTIQUES GENERALES' in line:
                in_stats = True
                continue
            elif '## TOP 10 PRODUITS' in line:
                in_stats = False
                in_products = True
                continue
            elif '## PATTERNS DETECTES' in line:
                in_products = False
                in_patterns = True
                continue
            
            if in_stats:
                if 'Connexions:' in line:
                    stats['connexions'] = int(line.split(':')[1].strip())
                elif 'Deconnexions:' in line:
                    stats['deconnexions'] = int(line.split(':')[1].strip())
                elif 'Recherches:' in line:
                    stats['recherches'] = int(line.split(':')[1].strip())
                elif 'Navigations:' in line:
                    stats['navigations'] = int(line.split(':')[1].strip())
                elif 'Ajouts panier:' in line:
                    stats['ajouts_panier'] = int(line.split(':')[1].strip())
                elif 'Achats:' in line:
                    stats['achats'] = int(line.split(':')[1].strip())
                elif 'Taux conversion:' in line and '%' in line:
                    stats['taux_conversion'] = float(line.split(':')[1].strip().replace('%', ''))
            
            elif in_products:
                if ':' in line and line.strip() and not line.startswith('#'):
                    parts = line.split(':')
                    if len(parts) == 2:
                        product = parts[0].strip()
                        count = int(parts[1].strip())
                        stats['top_products'].append({'product': product, 'count': count})
            
            elif in_patterns:
                if line.strip() and line.startswith('{'):
                    try:
                        pattern = json.loads(line)
                        pattern_type = pattern.get('pattern', 'Unknown')
                        if pattern_type in stats['patterns']:
                            stats['patterns'][pattern_type] += 1
                    except:
                        pass
        
        return stats
    
    except Exception as e:
        return None


def check_kafka_status():
    """Vérifie le statut de Kafka"""
    try:
        cmd = 'docker exec kafka kafka-topics --list --bootstrap-server localhost:9092'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        
        topics = [t.strip() for t in result.stdout.split('\n') if t.strip()]
        
        return {
            'status': 'running' if result.returncode == 0 else 'error',
            'topics': topics,
            'topic_count': len(topics)
        }
    except Exception as e:
        return {'status': 'error', 'topics': [], 'topic_count': 0, 'error': str(e)}


def get_docker_services():
    """Vérifie quels services Docker sont actifs"""
    try:
        cmd = 'docker ps --format "{{.Names}}\t{{.Status}}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        services = {}
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 2:
                    name = parts[0]
                    status = 'running' if 'Up' in parts[1] else 'stopped'
                    services[name] = status
        
        return services
    except Exception as e:
        return {}


if __name__ == "__main__":
    # Test des fonctions
    print("=== Test HDFS ===")
    print(get_hdfs_stats())
    
    print("\n=== Test MapReduce ===")
    print(get_mapreduce_results())
    
    print("\n=== Test E-commerce ===")
    print(get_ecommerce_insights())
    
    print("\n=== Test Kafka ===")
    print(check_kafka_status())
    
    print("\n=== Test Docker ===")
    print(get_docker_services())
