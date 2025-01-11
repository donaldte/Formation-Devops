from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configurer Selenium WebDriver
driver = webdriver.Chrome()  # Assurez-vous que le driver Chrome est installé
url = "https://www.google.com/search?kgmid=/g/1q67g_hzc&hl=en-CM&q=All%C3%B4+mon+Coco+Pointe-Claire&shndl=30&source=sh/x/loc/osrp/m5/1&kgs=dba304db80b2b63a#"
driver.get(url)

# Attendre que la page charge
time.sleep(5)

# Cliquer sur le bouton pour afficher tous les avis
try:
    driver.find_element(By.PARTIAL_LINK_TEXT, 'avis').click()
    time.sleep(5)
except Exception as e:
    print("Erreur:", e)

# Extraire les avis
reviews = []
review_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
for review in review_elements:
    try:
        name = review.find_element(By.CSS_SELECTOR, ".d4r55").text
        rating = review.find_element(By.CSS_SELECTOR, "span:first-child").get_attribute("aria-label")
        comment = review.find_element(By.CSS_SELECTOR, ".Jtu6Td").text
        date = review.find_element(By.CSS_SELECTOR, ".dehysf").text

        reviews.append({
            "Nom": name,
            "Note": rating,
            "Commentaire": comment,
            "Date": date
        })
    except Exception as e:
        print("Erreur d'extraction:", e)

# Sauvegarder dans un fichier Excel
df = pd.DataFrame(reviews)
df.to_excel("avis_allo_mon_coco.xlsx", index=False)
print("Extraction terminée. Fichier enregistré sous 'avis_allo_mon_coco.xlsx'.")

# Fermer le navigateur
driver.quit()
