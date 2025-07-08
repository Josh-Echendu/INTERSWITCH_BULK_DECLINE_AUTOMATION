# dispute_processor.py
import os
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from modal_clean_up import handle_modal_clean_up
from close_button import handle_close_button_clean_up
from decline import handle_decline_button_clean_up
from dispute_search_handler import matching_code, perform_search
from shared_data import skipped_log_code


FOLDER_PATH = r"C:\Users\Admin\Music\New folder\BETA_JOURNAL"

def load_dispute_codes():
    file_list = glob.glob(os.path.join(FOLDER_PATH, "*.jpg"))
    return [os.path.basename(f).split('.')[0] for f in file_list]

def process_disputes(driver, wait, log_code_list=None):
    if log_code_list:
        base_names = log_code_list
    else:
        base_names = load_dispute_codes()
        print(base_names)
    count = 0

    for code in base_names:
        print(f"Processing code: {code}, Remaining in skipped list: {skipped_log_code}")
        if count > 0 and count % 10 == 0:
            _refresh(driver, wait) 
        count += 1
        print('count: ', count)

        if not input_log_code(driver, wait, code):
            _refresh(driver, wait, code)
            continue

        if not click_search(driver, wait, code):
            _refresh(driver, wait, code)
            continue

        if not validate_code(driver, wait, code):
            _refresh(driver, wait, code)
            continue

        handle_modal(driver, wait, code)

def skipped_transactions(driver, wait):
    print('list of skipped log_codes: ', skipped_log_code)
    while skipped_log_code:
        # Store current skipped list and clear it
        current_skipped = skipped_log_code.copy()
        skipped_log_code.clear()
        process_disputes(driver, wait, current_skipped)
    return    

def _refresh(driver, wait, code=None):
    try:
        if code:
            print('before append: ', skipped_log_code)
            skipped_log_code.append(code)
            print('after append: ', skipped_log_code)

        print("Refreshing browser...")
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='logCode']")))
    except Exception as e:
        print(f"Refresh failed: {e}")

def input_log_code(driver, wait, code):
    try:
        log_code_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='logCode']")))
        driver.execute_script("arguments[0].value = '';", log_code_input)
        wait.until(lambda d: log_code_input.get_attribute('value') == '')
        log_code_input.send_keys(code)
        return True
    except Exception as e:
        print(f"[{code}] Failed to input log code: {e}")
        return False

def click_search(driver, wait, code):
    try:
        return perform_search(wait, driver, code)
    except Exception as e:
        print(f"[{code}] Failed on search: {e}")
        return False

def validate_code(driver, wait, code):
    try:
        cells = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "(//div//div[@class='rt-td'])")))
        extracted_log_code = cells[1].text.strip()
        print(cells[1].text.strip())
        return matching_code(extracted_log_code, wait, driver, code)
    except Exception as e:
        print(f"[{code}] Validation failed: {e}")
        return False

def handle_modal(driver, wait, code):
    file_path = os.path.join(FOLDER_PATH, f"{code}.jpg")
    try:
        react_pop_up = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ReactModal__Content ReactModal__Content--after-open']")))
        print(react_pop_up.get_attribute('innerHTML'))

        # this code is not redundant, itsa a wait mechinsm for all buttons to load unless no button would load
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dispute-modal-actions']/button")))

        decline_btns = react_pop_up.find_elements(By.XPATH, "//div[@class='dispute-modal-actions']/button[text()='Decline']")
        close_btns = react_pop_up.find_elements(By.XPATH, "//div[@class='dispute-modal-actions']/button[text()='CLOSE']")

        for c in close_btns:
            print(c.get_attribute('innerHTML'))

        for d in decline_btns:
            print(d.get_attribute("innerHTML"))

        if decline_btns and close_btns:
            print("Decline button found.")
            handle_decline_button_clean_up(driver, wait, code, close_btns, file_path, react_pop_up)
        elif close_btns:
            print("CLOSE button found.")
            handle_close_button_clean_up(driver, wait, code, close_btns, file_path)
        else:
            print(f"No actionable buttons found for {code}")
            handle_modal_clean_up(driver, wait, code)

    except Exception:
        print(f"[{code}] Modal handling failed.")
        handle_modal_clean_up(driver, wait, code)
