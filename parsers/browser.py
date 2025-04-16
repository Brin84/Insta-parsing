from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def login_phase(driver):
    print("[~] Открой браузер и войди в Instagram вручную.")
    driver.get("https://www.instagram.com/")
    input("🔑 После входа нажми Enter, чтобы продолжить...")