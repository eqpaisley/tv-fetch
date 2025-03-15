import requests
import json

API_KEY = "1319dc2e"  # Replace with your actual API key
BASE_URL = "http://www.omdbapi.com/"

def get_tv_show_details(title):
    """Fetch TV show details from OMDb API"""
    params = {
        "t": title,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code == 200 and "Metascore" in data and data["Metascore"] != "N/A":
        try:
            if int(data["Metascore"]) > 62:
                return {
                    "Title": data["Title"],
                    "Year": data["Year"],
                    "Metascore": data["Metascore"],
                    "IMDb_ID": data["imdbID"]
                }
        except ValueError:
            pass  # Skip if Metascore is not a valid number
    return None

def main():
    tv_shows = ["Breaking Bad", "Stranger Things", "The Office", "Sherlock", "Fargo"]  # Add more titles here
    filtered_shows = []

    for show in tv_shows:
        details = get_tv_show_details(show)
        if details:
            filtered_shows.append(details)
    
    # Save the filtered list as JSON
    with open("tv_shows_sonarr.json", "w") as f:
        json.dump(filtered_shows, f, indent=4)

    print(f"Saved {len(filtered_shows)} TV shows with Metascore > 62 to tv_shows_sonarr.json")

if __name__ == "__main__":
    main()
