from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time
import requests

# Set up directories to store JSON files
match_types = ['test', 'odi', 't20', 'ipl']
base_dir = 'data'
os.makedirs(base_dir, exist_ok=True)
for match in match_types:
    os.makedirs(os.path.join(base_dir, f"{match}_matches"), exist_ok=True)

# Selenium setup (you need to have ChromeDriver installed)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=Service(), options=options)

# Go to the Cricsheet matches page
driver.get("https://cricsheet.org/matches/")
time.sleep(3)

# Loop through match types and download JSON files
for match_type in match_types:
    print(f"Processing: {match_type.upper()}")

    # Find all links for this match type
    links = driver.find_elements(By.XPATH, f"//a[contains(@href, '/download/{match_type}_')]")
    
    for link in links:
        href = link.get_attribute('href')
        if href.endswith('.json'):
            filename = href.split('/')[-1]
            save_path = os.path.join(base_dir, f"{match_type}_matches", filename)

            # Skip if already downloaded
            if not os.path.exists(save_path):
                try:
                    response = requests.get(href)
                    if response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded: {filename}")
                    else:
                        print(f"Failed to download: {href}")
                except Exception as e:
                    print(f"Error downloading {href}: {str(e)}")

driver.quit()
