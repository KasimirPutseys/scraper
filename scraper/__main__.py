import typer
from scraper.scraper import TransfermarktScraper

app = typer.Typer()

@app.command()
def run_etl(url: str):
    db_config = {
        "dbname": "transfers",
        "user": "user",
        "password": "password",
        "host": "localhost",
        "port": "5432"
    }
    scraper = TransfermarktScraper(db_config)
    soup = scraper.extract(url)
    player_data = scraper.transform(soup)
    scraper.load(player_data)

if __name__ == "__main__":
    app()
