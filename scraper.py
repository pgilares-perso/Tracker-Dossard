import os
import requests
from bs4 import BeautifulSoup

# Récupération de vos secrets GitHub
URL = os.environ.get('URL_COURSE')
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def envoyer_alerte(nombre_dossards):
    message = f"🚨 ALERTE : {nombre_dossards} dossard(s) disponible(s) à la revente !\nFoncez ici : {URL}"
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': message})

def verifier_page():
    # On se fait passer pour un vrai navigateur web
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        reponse = requests.get(URL, headers=headers)
        reponse.raise_for_status()
        
        # On analyse le code HTML de la page
        soup = BeautifulSoup(reponse.text, 'html.parser')
        
        # On cible précisément le tableau grâce à sa classe "table-listados"
        tableau = soup.find('table', class_='table-listados')
        
        if tableau:
            # On cherche le corps du tableau
            tbody = tableau.find('tbody')
            
            # On compte le nombre de lignes <tr> présentes dans le tbody
            lignes_dossards = tbody.find_all('tr') if tbody else []
            
            if len(lignes_dossards) == 0:
                envoyer_alerte(len(lignes_dossards))
                print(f"Changement détecté : {len(lignes_dossards)} dossard(s) trouvé(s) ! Alerte envoyée.")
            else:
                print("Rien de nouveau. Le tableau est vide (0 dossard).")
        else:
            print("Erreur : Le tableau n'a pas été trouvé. La page a peut-être bloqué l'accès ou changé de structure.")
            
    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    verifier_page()
