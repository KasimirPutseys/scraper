mport requests
from bs4 import BeautifulSoup
import psycopg2
import logging
from datetime import datetime

class TransfermarktScraper:
    def __init__(self, db_config):
        self.db_config = db_config

    def extract(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def transform(self, soup):
        if soup is None:
            return None
        try:
            name = soup.find('h1').text.strip()
            club = soup.find('div', class_='club-name').text.strip() if soup.find('div', class_='club-name') else "Unknown"
            value = soup.find('div', class_='market-value').text.strip() if soup.find('div', class_='market-value') else "N/A"
            age = int(soup.find('span', class_='age').text.strip()) if soup.find('span', class_='age') else 0
            position = soup.find('div', class_='position').text.strip() if soup.find('div', class_='position') else "Unknown"
            return {
                "name": name,
                "club": club,
                "market_value": value,
                "age": age,
                "position": position,
                "last_updated": datetime.now()
            }
        except Exception as e:
            logging.error(f"Error transforming data: {e}")
            return None

    def load(self, player_data):
        if player_data is None:
            return
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO players (name, club, market_value, age, position, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (player_data['name'], player_data['club'], player_data['market_value'],
                 player_data['age'], player_data['position'], player_data['last_updated'])
            )
            conn.commit()
            cur.close()
            conn.close()
            logging.info("Player data loaded successfully.")
        except Exception as e:
            logging.error(f"Database load error: {e}")