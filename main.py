from driver_manager import get_driver
from auth import login, navigate_to_disputes
from dispute_processor import process_disputes, skipped_transactions
from selenium.webdriver.support.ui import WebDriverWait


def main():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    login(driver, wait)

    navigate_to_disputes(driver, wait)
    process_disputes(driver, wait)
    skipped_transactions(driver, wait)

    print("All disputes processed.")
    driver.quit()

if __name__ == "__main__":
    main()
