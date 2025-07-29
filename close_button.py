import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_close_button(driver, wait, close_buttons, value_u):
    try:
        driver.execute_script("arguments[0].click();", close_buttons)
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        ))
        print(f"{value_u}: already Declined")

        return True
    except Exception as e:
        print(f"[{value_u}] Failed to close modal using CLOSE button: {e}")
        return False

def force_remove_modal(driver, wait, value_u):
    try:
        modal = driver.find_element(By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        driver.execute_script("arguments[0].remove();", modal)
        print(f"[{value_u}] Forcefully removed modal popup from DOM")
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        ))
        return True
    except Exception as e:
        print(f"[{value_u}] Failed to remove modal via JS: {e}")
        return False

def refresh_page(driver, value_u):
    try:
        driver.refresh()
        print(f"[{value_u}] Refreshing webpage...")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='logCode']"))) 
    except Exception as e:
        print(f"[{value_u}] Refresh failed: {e}")

def handle_close_button_clean_up(driver, wait, value_u, close_buttons, file_path=None):
    if click_close_button(driver, wait, close_buttons, value_u):
        return

    # Close button failed, try force-removal
    if force_remove_modal(driver, wait, value_u):
        return

    # Force removal failed, try refreshing the page
    refresh_page(driver, value_u)
