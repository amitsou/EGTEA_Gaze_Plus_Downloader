from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import time


def initialize_driver():
    download_dir = os.path.dirname(os.path.realpath(__file__))
    options = Options()
    # options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir
    })
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def click_skip_button(driver):
    try:
        skip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'dig-Button-content') and contains(text(), 'Skip')]")))
        skip_button.click()
    except Exception as e:
        print("Skip button not found or not clickable. Exiting.")
        driver.quit()


def click_download_button(driver):
    try:
        file_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'dig-Button') and "
                           "contains(@class, 'dig-Button--borderless') and "
                           "contains(@class, 'dig-Button--standard') and "
                           "contains(@class, 'ekabin11') and contains(@class, 'ekabin1c') and "
                           "contains(@class, 'ekabin17') and contains(@class, 'ekabin1un') and "
                           "contains(@class, '_4rjmw90') and contains(@class, '_titlebar-dropdowns__button_l0wdg_7')]")))

        ActionChains(driver).move_to_element(file_button).click(file_button).perform()

        download_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download')]")))
        download_option.click()

        try:
            continue_download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(@class, 'dig-Button-content') and "
                               "contains(text(), 'Or continue with download only')]")))
            continue_download_button.click()
        except Exception as e:
            print("Continue download button not found or not clickable. Exiting.")
            driver.quit()

    except Exception as e:
        print(e)
        driver.quit()


if __name__ == "__main__":
    URL = "https://www.dropbox.com/s/w260trfnhdfcooh/Recipes.pdf?dl=0"

    driver = initialize_driver()
    driver.maximize_window()
    driver.get(URL)

    click_skip_button(driver)
    click_download_button(driver)

    time.sleep(10)
    driver.quit()
