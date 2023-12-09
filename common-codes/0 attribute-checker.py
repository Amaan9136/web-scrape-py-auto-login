# use this when u think attributes(login details from html) are wrong so that u can verify everything line by line
# only do this if u dont know the exact login details from html else it is waste of time

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#login with your number and get credentials, login_url, profile_url, app_login_mobile, app_login_password, app_login_button, balance_attribute
credentials = [('7353346164', '7353346164s')]
login_url = "https://www.lzpcue00-oecu.com/index/user/login.html"
profile_url = "https://www.lzpcue00-oecu.com/index/my/index.html"  # Profile URL
app_login_mobile= "tel"
app_login_password= "pwd"
app_login_button= "login"
balance_attribute= 'small[data-v-d5f15326]'
income_attribute = "//div[contains(text(), 'Balance')]/following-sibling::div[2]"


# Function to print source code in case of Errors/Exceptions
def print_source_code(driver):
    source_code = driver.page_source
    body_start = source_code.find('<body')
    body_end = source_code.find('</body') + 7
    print(f"Check Source code!")
    print(f"Source Code:\n{source_code[body_start:body_end]}")

# Function to verify attributes
def verify_attributes():
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)

    driver.get(login_url)
    wait = WebDriverWait(driver, 10)

    for mobile, password in credentials:
        try:
            start_page = driver.current_url
            print(f'\nChecking for {mobile}...')
            try:
                mobile_field = wait.until(EC.presence_of_element_located((By.NAME, app_login_mobile)))
                print(f"Mobile attribute found: {mobile_field.get_attribute('name')}")
            except NoSuchElementException:
                print(f"Login failed for {mobile}.")

            try:
                password_field = driver.find_element(By.NAME, app_login_password)
                print(f"Password attribute found: {password_field.get_attribute('name')}")
            except NoSuchElementException:
                print(f"Login Password attribute not found for {mobile}!")

            try:
                login_button = driver.find_element(By.CLASS_NAME, app_login_button)
                print(f"Login button attribute found: {login_button.get_attribute('class')}")
            except NoSuchElementException:
                print(f"Login Button attribute not found for {mobile}!")

            # Attempt to log in
            mobile_field.send_keys(mobile)
            password_field.send_keys(password)
            login_button.click()

            for _ in range(10):  # loop till we login
                if driver.current_url != start_page:
                    break
                time.sleep(0.5)

            success_page_url = driver.current_url
            if success_page_url == start_page:
                print(f"Login failed for {mobile}.")
            else:
                print(f"Login successful for {mobile}.")
                driver.get(profile_url)

                for _ in range(10):
                    if driver.current_url == profile_url:
                        print(f"{mobile} is in profile page!")
                        break
                    time.sleep(0.5)

                try:
                    balance_element = driver.find_element(By.CSS_SELECTOR, balance_attribute)
                    print(f"Balance attribute found: {balance_attribute} with {balance_element.text}")
                except NoSuchElementException:
                    print(f"Profile Balance attribute not found for {mobile}!")
                try:
                    income_element = driver.find_element(By.XPATH, income_attribute)
                    print(f"Balance attribute found: {income_attribute} with {income_element.text}")
                except NoSuchElementException:
                    print(f"Profile Income attribute not found for {mobile}!")

        except Exception:
            print_source_code(driver)

        finally:
            driver.quit()


if __name__ == '__main__':
    verify_attributes()
