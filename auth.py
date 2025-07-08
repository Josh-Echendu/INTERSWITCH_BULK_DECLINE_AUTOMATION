# auth.py
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from authnetication import password, email


def login(driver, wait):
    # an infinit look incase network gets poor
    while True:
        try:
            driver.get("https://passport.interswitchng.com/passport/login")
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
            wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']"))).submit()
            print(f"{email}, Logged in successfully")
            break

        except Exception as e:
            print(f"Network issue or page load failure: {e}")
            driver.refresh()
            print("Refreshing ...")
            time.sleep(5)


def navigate_to_disputes(driver, wait):
    # an infinite look incase network gets poor
    while True:
        try:
            print("Navigating to Disputes page...")
            driver.get("https://portal.interswitchng.com/portal/arbiter/app/disputemgmt/disputes")
            
            # Wait until the dropdown is clickable (this confirms the page loaded)
            drop_down_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='INSTITUTION: MONIEPOINT MICROFINANCE BANK']")
            ))
            print("Successfully loaded the Disputes page.")

            # Click the dropdown and navigate further
            driver.execute_script("arguments[0].click()", drop_down_button)

            team_apt_icon = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//ul//a[text()='TeamApt Limited']")
            ))
            driver.execute_script("arguments[0].click()", team_apt_icon)

            dispute = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div//a//span[text()='Disputes']")
            ))
            driver.execute_script("arguments[0].click()", dispute)

            # Successfully navigated all the way
            break

        except Exception as e:
            print(f"Network issue or page load failure: {e}")
            print("Refreshing ...")
            driver.refresh()
            time.sleep(5)
