import requests
import json
from datetime import datetime, timedelta

# OMDB API Key (replace with your actual key)
OMDB_API_KEY = "1319dc2e"

# Helper function to check if the show aired in the past 6 months
def is_recent_release(release_date):
    if not release_date:
        return False  # Skip if no release date

    try:
        air_date = datetime.strptime(release_date, "%d %b %Y")  # Format: "01 Jan 2024"
        six_months_ago = datetime.today() - timedelta(days=180)
        return air_date >= six_months_ago
    except ValueError:
        return False  # Skip invalid dates

# List of TV show IMDb IDs (we may need another API to get a dynamic list)
tv_show_ids = ["tt0944947", "tt0903747", "tt7366338"]  # Example IMDb IDs

filtered_shows = []

for imdb_id in tv_show_ids:
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        metascore = data.get("Metascore", "0")

        if metascore.isdigit() and int(metascore) > 62 and is_recent_release(data.get("Released")):
            filtered_shows.append({
                "title": data.get("Title"),
                "year": data.get("Year"),
                "imdb_id": data.get("imdbID"),
                "metascore": int(metascore),
                "release_date": data.get("Released"),
            })

# Save the filtered list to JSON
output_file = "tv_shows_sonarr.json"
with open(output_file, "w") as f:
    json.dump(filtered_shows, f, indent=4)

print(f"Saved {len(filtered_shows)} TV shows to {output_file}")
