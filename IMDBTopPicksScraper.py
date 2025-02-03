import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_top_movies():
    # Set up Chrome WebDriver with a mobile User-Agent
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Fix for headless mode issue
    options.add_argument("--use-gl=swiftshader")  # Use software rendering instead of GPU
    options.add_argument("--disable-features=VizDisplayCompositor")  # Prevent GPU issues
    options.add_argument("--window-size=375,812")  # Mobile viewport size
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36")
    
    # Launch WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    URL = "https://m.imdb.com/chart/moviemeter/"  # Mobile version
    driver.get(URL)
    
    try:
        # Wait for the movie list to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list li a.ipc-lockup-overlay")))
        
        movies = []
        # Locate movie elements in the mobile version
        movie_items = driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list li a.ipc-lockup-overlay")
        
        if not movie_items:
            print("No movie titles found. IMDb structure may have changed or request is blocked.")
            return []
        
        for item in movie_items:
            title = item.get_attribute("aria-label").replace("View title page for ", "").strip()
            link = item.get_attribute("href")
            if title:
                movies.append({"Top Picks": title, "IMDB Link": link})
    
    finally:
        driver.quit()  # Close the browser
    
    return movies

def save_to_excel(movies, filename="C:/Users/Marian/Desktop/IMDb_Top_Picks.xlsx"):
    df = pd.DataFrame(movies)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    movies = get_top_movies()
    if movies:
        save_to_excel(movies)
    else:
        print("No movies found. Check if IMDb is blocking the request.")
