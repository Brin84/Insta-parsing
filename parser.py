from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os


def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login_insta(driver):
    print("[~] Открой браузер и войди в Instagram вручную.")
    driver.get("https://www.instagram.com/")
    input("🔑 После входа нажми Enter...")

def scroll_followers(driver, target_username, scroll_limit=100):
    print(f"[~] Открываю профиль {target_username}...")
    driver.get(f"https://www.instagram.com/{target_username}/")
    time.sleep(5)

    try:
        followers_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]"))
        )
        followers_button.click()
    except Exception as e:
        print("⚠️ Не удалось найти кнопку подписчиков.")
        print("Ошибка:", e)
        return []

    input("🔁 Прокрути список подписчиков вручную до конца, затем нажми Enter...")

    html = driver.page_source
    os.makedirs("debug", exist_ok=True)
    with open("debug/followers_final.html", "w", encoding="utf-8") as f:
        f.write(html)


    soup = BeautifulSoup(html, "html.parser")
    usernames = set()


    for a in soup.find_all("a", href=True):
        href = a["href"]

        if href.count("/") == 2 and href.startswith("/") and not any(
                x in href for x in ["explore", "accounts", "reels", "p/", "stories", "direct"]):
            username = href.strip("/").split("/")[0]
            if username and username != target_username:
                usernames.add(username)

    print(f"[✓] Собрано логинов: {len(usernames)}")
    return list(usernames)

def save_to_csv(usernames, filename="followers_list.csv"):
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/" + filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        for username in usernames:
            writer.writerow([username])
    print(f"[✓] Сохранено в data/output/{filename}")

if __name__ == "__main__":
    print("=== Instagram Followers Parser  ===")
    driver = setup_driver()
    login_insta(driver)

    target = input("Введите username аккаунта для сбора подписчиков: ").strip()
    followers = scroll_followers(driver, target, scroll_limit=50)
    save_to_csv(followers)