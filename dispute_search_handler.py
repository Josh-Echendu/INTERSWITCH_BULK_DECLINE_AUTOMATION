from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def matching_code(log_code_value, wait, driver, value_u):
    """Check if the log code matches, retry search up to 3 times."""
    max_attempts = 3

    for attempt in range(3):
        if is_log_code_matching(log_code_value, value_u):
            return try_show_dropdown(wait, driver, value_u)

        print(f"[Attempt {attempt + 1}] Log code doesn't match. Performing search...")
        if not perform_search(wait, driver, value_u):
            print(f"[{value_u}] Search failed on attempt {attempt}")
            return False

        log_code_value = get_new_log_code(wait)
        print(f"[Attempt {attempt + 1}] Retrieved new log code: {log_code_value}")

    print(f"[{value_u}] Max attempts reached without match.")
    return False


def is_log_code_matching(current_code, target_code):
    """Check if the current log code matches the expected one."""
    return current_code == target_code


def try_show_dropdown(wait, driver, value_u):
    """Attempt to click the dropdown."""
    try:
        dropdown_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='1']")))
        driver.execute_script("arguments[0].click()", dropdown_element)
        print(f"[{value_u}] Log code matched and dropdown clicked successfully.")
        return True
    except Exception as e:
        print(f"[{value_u}] Failed to click dropdown: {e}")
        return False


def perform_search(wait, driver, value_u):
    """Click the search button after ensuring modal is not visible."""
    try:
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")))
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='searchButton']")))
        driver.execute_script("arguments[0].click()", search_button)
        print('searched code searched successfully')
        return True
    except Exception as e:
        print(f"[{value_u}] Search action failed: {e}")
        return False


def get_new_log_code(wait):
    """Retrieve the updated log code value after search."""
    log_code_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "(//div//div[@class='rt-td'])")))
    return log_code_elements[1].text
