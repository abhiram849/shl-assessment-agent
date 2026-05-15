from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json
import time
import os


BASE_URL = "https://www.shl.com"

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


# Launch Chrome browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)


print("Opening SHL catalog...")

driver.get(CATALOG_URL)

time.sleep(5)


# -----------------------------
# Scroll page to load all items
# -----------------------------

print("Scrolling to load all assessments...")

last_height = driver.execute_script(
    "return document.body.scrollHeight"
)

for _ in range(20):

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(3)

    new_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    if new_height == last_height:
        break

    last_height = new_height


# -----------------------------
# Collect assessment URLs
# -----------------------------

print("Collecting assessment links...")

assessment_urls = set()

links = driver.find_elements(By.TAG_NAME, "a")

for i in range(len(links)):

    try:

        links = driver.find_elements(By.TAG_NAME, "a")

        href = links[i].get_attribute("href")

        if href and "/products/product-catalog/view/" in href:

            assessment_urls.add(href)

    except Exception:
        continue


assessment_urls = list(assessment_urls)


print(f"\nFound {len(assessment_urls)} assessments\n")


# -----------------------------
# Scrape assessment details
# -----------------------------

all_assessments = []


for index, url in enumerate(assessment_urls, start=1):

    try:

        print(f"[{index}] Opening: {url}")

        driver.get(url)

        time.sleep(3)

        # Assessment title
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except:
            title = "Unknown"


        # Description paragraphs
        paragraphs = driver.find_elements(By.TAG_NAME, "p")

        description = " ".join(
            [p.text.strip() for p in paragraphs[:8] if p.text.strip()]
        )


        # Optional metadata
        page_text = driver.find_element(By.TAG_NAME, "body").text


        assessment = {
            "name": title,
            "url": url,
            "description": description,
            "content": page_text[:5000]
        }


        all_assessments.append(assessment)

        print(f"Scraped: {title}\n")


    except Exception as e:

        print(f"Error scraping {url}")
        print("Error:", e)
        print()


# -----------------------------
# Save JSON
# -----------------------------

os.makedirs("app/data", exist_ok=True)


with open(
    "app/data/assessments.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(all_assessments, f, indent=4, ensure_ascii=False)


print("\nSaved assessments.json successfully")


# Close browser
driver.quit()