import requests
import json
import csv
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Load variables from the .env file if it exists.
load_dotenv()

# We look for the API key in your system or the .env file.
# This makes it MUCH safer to share your code.
API_KEY = os.getenv("OPENSANCTIONS_API_KEY")

# The "match" endpoint is used for fuzzy searching (finds names even with typos).
# We use the "default" scope which covers Sanctions, PEPs, and Crime.
API_URL = "https://api.opensanctions.org/match/default"

def search_entity(name):
    """
    This function takes a name, sends it to the API, and returns the matches.
    """
    
    # We define what we are looking for. Here, we say it's a "Person" and give the name.
    # You can also add 'birth_date': ['1970'] inside properties for more accuracy.
    payload = {
        "queries": {
            "search_1": {
                "schema": "Person",
                "properties": {
                    "name": [name]
                }
            }
        }
    }

    # We send the API key in the 'headers' for security.
    headers = {
        "Authorization": f"ApiKey {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"--- Searching for: {name} ---")

    try:
        # This line actually 'calls' the API over the internet.
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # If the API says 'OK' (status code 200), we process the data.
        if response.status_code == 200:
            data = response.json()
            
            # The API returns a list of results for our specific query 'search_1'.
            results = data.get("responses", {}).get("search_1", {}).get("results", [])
            
            if not results:
                print("No matches found.")
                return []

            print(f"Found {len(results)} potential matches.")
            return results
        else:
            print(f"Error: The API returned status code {response.status_code}")
            print(response.text)
            return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def save_to_csv(results, filename="sanctions_results.csv"):
    """
    This function takes the results and saves them into a spreadsheet (CSV).
    """
    if not results:
        return

    # These are the columns we want in our spreadsheet.
    fieldnames = ['Name', 'Score', 'ID', 'Schema', 'Topics']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in results:
            # We extract specific pieces of information to make the CSV clean.
            writer.writerow({
                'Name': item.get('caption'),
                'Score': item.get('score'),
                'ID': item.get('id'),
                'Schema': item.get('schema'),
                'Topics': ", ".join(item.get('properties', {}).get('topics', []))
            })
    
    print(f"Results saved to {filename}")

# --- MAIN EXECUTION ---
# This part tells the script what to do when you run it.
if __name__ == "__main__":
    # CHANGE THIS NAME to whoever you want to check!
    target_name = "Vladimir Putin"
    
    # 1. Run the search
    found_matches = search_entity(target_name)
    
    # 2. Print matches to the screen so you can see them immediately.
    for match in found_matches:
        # 'score' is how confident the API is (1.0 is a perfect match).
        print(f"Match Found: {match['caption']} | Score: {match['score']}")
    
    # 3. Save matches to a file you can open in Excel.
    save_to_csv(found_matches)
