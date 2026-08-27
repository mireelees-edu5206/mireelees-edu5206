#!/usr/bin/env python3
"""
Script para hacer web scraping de contribuciones de GitHub.
- Extrae fechas y niveles de contribución
- Guarda en JSON para renderizado posterior
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta

def fetch_contributions(username='eledu', output_path='data/contributions.json'):
    """
    Obtiene contribuciones de GitHub mediante web scraping.
    
    Args:
        username: Nombre de usuario de GitHub
        output_path: Ruta donde guardar el JSON
    """
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # URL de contribuciones
    url = f'https://github.com/users/{username}/contributions'
    
    print(f"Obteniendo contribuciones de {url}...")
    
    # Headers para simular navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todos los rectángulos de contribución
        contributions = []
        
        # GitHub usa elementos <rect> o <td> con data-level
        contribution_elements = soup.find_all('rect', {'data-level': True})
        
        if not contribution_elements:
            # Intentar con formato alternativo
            contribution_elements = soup.find_all('td', {'data-level': True})
        
        if contribution_elements:
            for elem in contribution_elements:
                date = elem.get('data-date')
                level = elem.get('data-level')
                count = elem.get('data-count', '0')
                
                if date and level:
                    contributions.append({
                        'date': date,
                        'level': int(level),
                        'count': int(count)
                    })
        else:
            print("No se encontraron elementos de contribución. Generando datos de ejemplo...")
            contributions = generate_sample_data()
        
        # Ordenar por fecha
        contributions.sort(key=lambda x: x['date'])
        
        # Guardar en JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(contributions, f, indent=2)
        
        print(f"Contribuciones guardadas en {output_path}")
        print(f"Total de días con contribuciones: {len(contributions)}")
        
    except requests.RequestException as e:
        print(f"Error al obtener contribuciones: {e}")
        print("Generando datos de ejemplo...")
        contributions = generate_sample_data()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(contributions, f, indent=2)
        
        print(f"Datos de ejemplo guardados en {output_path}")

def generate_sample_data():
    """
    Genera datos de ejemplo para el mapa de calor.
    """
    contributions = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    current_date = start_date
    while current_date <= end_date:
        # Generar nivel aleatorio (0-4)
        import random
        level = random.choices([0, 1, 2, 3, 4], weights=[0.3, 0.3, 0.2, 0.15, 0.05])[0]
        count = level * random.randint(1, 5)
        
        contributions.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'level': level,
            'count': count
        })
        
        current_date += timedelta(days=1)
    
    return contributions

if __name__ == "__main__":
    fetch_contributions()
