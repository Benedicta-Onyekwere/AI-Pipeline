import requests
from bs4 import BeautifulSoup
import csv
import time

# --- STEP 1: SET UP THE BASICS ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

BASE_URL = "https://www.europarl.europa.eu/committees/en/droi/home/members"

def scrape_meps():
    print("Starting the scraper... please wait.")
    
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We look for all the MEP "cards" on the page
    mep_cards = soup.find_all('div', class_='es_member-list-item')
    
    if not mep_cards:
        # Try finding by the other class seen in HTML
        mep_cards = soup.find_all('div', class_='erpl_member-list-item')

    if not mep_cards:
        print("No MEP cards found. The website structure might have changed or requires JavaScript.")
        return

    print(f"Found {len(mep_cards)} total MEPs (Full Members + Substitutes). Fetching individual details...")
    
    all_data = []

    for card in mep_cards:
        # Find name and link
        name_tag = card.find('div', class_='es_title-h4') or card.find('div', class_='erpl_title--h4')
        link_tag = card.find('a', href=True)
        
        if name_tag and link_tag:
            mep_name = name_tag.get_text(strip=True)
            profile_url = link_tag['href']
            
            if not profile_url.startswith("http"):
                profile_url = "https://www.europarl.europa.eu" + profile_url
            
            # Fetch deep info
            mep_details = scrape_profile(profile_url)
            mep_details['Name'] = mep_name
            mep_details['Profile URL'] = profile_url
            
            all_data.append(mep_details)
            
            # Print progress
            print(f"  > Scraped: {mep_name}")
            
            # Politeness delay
            time.sleep(0.3)

    save_to_csv(all_data)
    print(f"\nSuccess! Found {len(all_data)} MEPs. Data is saved in 'mep_details.csv'")

def scrape_profile(url):
    """Goes inside a single MEP's profile page and extracts data."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        s = BeautifulSoup(res.text, 'html.parser')
        
        info = {
            "Country": "Not found",
            "Political Group": "Not found",
            "National Party": "Not found",
            "Role": "Not found",
            "Facebook": "Not found",
            "Twitter": "Not found",
            "Instagram": "Not found"
        }
        
        # Extract basic info
        group_tag = s.find('h3', class_='sln-political-group-name')
        if group_tag:
            info["Political Group"] = group_tag.get_text(strip=True)
            
        role_tag = s.find('p', class_='sln-political-group-role')
        if role_tag:
            info["Role"] = role_tag.get_text(strip=True)

        # Country and National Party are often in this div
        country_party_div = s.find('div', class_='es_title-h3 mt-1 mb-1')
        if country_party_div:
            text = country_party_div.get_text(strip=True)
            if " - " in text:
                parts = text.split(" - ")
                info["Country"] = parts[0].strip()
                info["National Party"] = parts[1].strip()
            else:
                info["Country"] = text
        
        # Role in Committee
        # Often structured as: <h4 class="es_title-h4">Role</h4> ... <div class="erpl_committee">Committee Name</div>
        committees = s.find_all('div', class_='erpl_committee')
        committee_role = "Not found"
        for comm in committees:
            if "Subcommittee on Human Rights" in comm.get_text():
                # The role is usually in the preceding h4
                role_header = comm.find_previous('h4', class_='es_title-h4')
                if role_header:
                    committee_role = role_header.get_text(strip=True)
                break
        info["Committee Role"] = committee_role
        
        # Social Media
        fb = s.find('a', class_='link_fb')
        if fb: info["Facebook"] = fb['href']
        
        tw = s.find('a', class_='link_twitt')
        if tw: info["Twitter"] = tw['href']
        
        inst = s.find('a', class_='link_instag')
        if inst: info["Instagram"] = inst['href']
        
        return info
    except Exception as e:
        return {"Country": "Error", "Political Group": "Error", "Role": "Error"}


def save_to_csv(data):
    if not data:
        return
    keys = data[0].keys()
    with open('mep_details.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)

        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    scrape_meps()
