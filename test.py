import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup(driver_path):
    return webdriver.Chrome(service=Service(driver_path))


def scrape_imdb_top_movies(driver_path):
    driver = setup(driver_path)
    driver.get("https://www.imdb.com/chart/top/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"))
    )

    data = []
    for container in driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"):
        row = {"rank": np.nan, "title": np.nan, "release_year": np.nan, "duration": np.nan,
               "rate_type": np.nan, "star_rating": np.nan, "rated_by": np.nan}

        try:
            rank_title = container.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
            row["rank"], row["title"] = rank_title.split(". ", 1)
        except:
            pass

        try:
            metadata = container.find_elements(By.CSS_SELECTOR, "span.cli-title-metadata-item")
            row["release_year"] = metadata[0].text if len(metadata) >= 1 else np.nan
            row["duration"] = metadata[1].text if len(metadata) >= 2 else np.nan
            row["rate_type"] = metadata[2].text if len(metadata) >= 3 else np.nan
        except:
            pass

        try:
            row["star_rating"] = container.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
        except:
            pass

        try:
            row["rated_by"] = container.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text
        except:
            pass

        data.append(row)

    driver.quit()
    return pd.DataFrame(data)


# Run scraper
df = scrape_imdb_top_movies("/Users/mac/Downloads/chromedriver-mac-arm64 2/chromedriver")

print(df.shape)  # Should show (250, 7)

# Save to CSV (always works)
df.to_csv("imdb_top_movies.csv", index=False)

# Save to Excel (requires openpyxl)
try:
    df.to_excel("imdb_top_movies.xlsx", index=False)
    print("Excel file saved ✅")
except ImportError:
    print("⚠️ Install openpyxl to save as Excel: pip install openpyxl")