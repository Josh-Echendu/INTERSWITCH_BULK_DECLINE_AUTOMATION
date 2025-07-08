import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from shared_data import skipped_log_code


def upload_evidence(wait, file_path):
    file_input = wait.until(EC.presence_of_element_located((By.ID, 'evidenceFiles')))
    file_input.send_keys(file_path)

def attach_evidence(wait):
    attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Attach Evidence']")))
    attach_button.click()

def decline_transaction(react_pop_up):
    decline_btn = react_pop_up.find_element(By.XPATH, "(//div[@class='dispute-modal-actions']/button)[3]")
    decline_btn.click()
    
    yes_btn = react_pop_up.find_element(By.XPATH, "//button[text()='YES']")
    yes_btn.click()

# def delete_file(file_path, value_u):
#     try:
#         os.remove(file_path)
#         print(f"{value_u}: File deleted successfully")
#     except Exception as e:
#         print(f"[{value_u}] Failed to delete file: {e}")
#         return False
#     return True

def force_remove_modal(driver, wait, value_u):
    try:
        modal = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")))
        driver.execute_script("arguments[0].remove();", modal)
        print(f"[{value_u}] Forcefully removed modal popup from DOM")
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")))
    except Exception as e:
        print(f"[{value_u}] Failed to remove modal via JS: {e}")
        refresh_page(driver, value_u)

def refresh_page(driver, value_u):
    try:
        driver.refresh()
        print(f"[{value_u}] Refreshing webpage...")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='logCode']"))) 
    except Exception as e:
        print(f"[{value_u}] Refresh failed: {e}")

def try_close_modal(driver, wait, close_buttons, value_u):
    try:
        driver.execute_script("arguments[0].click();", close_buttons[0])
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")))
    except Exception as e:
        print(f"[{value_u}] Close button failed: {e}")
        force_remove_modal(driver, wait, value_u)

def handle_decline_button_clean_up(driver, wait, value_u, close_buttons, file_path, react_pop_up):
    try:
        if not os.path.exists(file_path):
            print(f"[{value_u}] File not found: {file_path}")
            return

        upload_evidence(wait, file_path)
        attach_evidence(wait)
        decline_transaction(react_pop_up)

        print(f"{value_u}: successfully declined")
        print(f"{value_u}, transaction_ID marked for deletion")
        return 
        # if not delete_file(file_path, value_u):
        #     force_remove_modal(driver, wait, value_u)

    except Exception as e:
        print(f"[{value_u}] Decline process failed: {e}")
        print('before append: ', skipped_log_code)
        skipped_log_code.append(value_u)
        print('after append: ', skipped_log_code)
        if close_buttons:
            try_close_modal(driver, wait, close_buttons, value_u)
