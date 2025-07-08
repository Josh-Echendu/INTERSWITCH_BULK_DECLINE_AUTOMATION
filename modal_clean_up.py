from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from shared_data import skipped_log_code


def close_modal_with_x_button(driver, wait, value_u):
    """Attempt to close the modal using the X button."""
    try:
        x_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='mod-title']/i")))
        x_button.click()
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        ))
        print(f"[{value_u}] Modal closed with X button")
        return True
    except Exception as e:
        print(f"[{value_u}] Could not close modal with X button: {e}")
        return False

def force_remove_modal(driver, wait, value_u):
    """Force remove the modal using JavaScript."""
    try:
        modal = driver.find_element(By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        driver.execute_script("arguments[0].remove();", modal)
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")
        ))
        print(f"[{value_u}] Modal forcefully removed")
        return True
    except Exception as e:
        print(f"[{value_u}] Could not remove modal via JS: {e}")
        return False

def _refresh_page(driver, value_u):
    """Refresh the page as a last resort."""
    try:
        driver.refresh()
        print(f"[{value_u}] Refreshing page...")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='logCode']")))

    except Exception as e:
        print(f"[{value_u}] Refresh failed: {e}")

def handle_modal_clean_up(driver, wait, value_u):
    """Clean up modal using different fallback options."""
    print('before append: ', skipped_log_code)
    skipped_log_code.append(value_u)
    print('after append: ', skipped_log_code)
    if close_modal_with_x_button(driver, wait, value_u):
        return

    if force_remove_modal(driver, wait, value_u):
        return

    _refresh_page(driver, value_u)
