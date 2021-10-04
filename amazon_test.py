from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium import webdriver
from datetime import *
import time
import re
import sys


# Browser Options
options = Options()
options.add_argument("--window_size=1920x1080")

# Browser
driver = webdriver.Chrome('/Users/vjariya/cicd/deployment/QA_Scripts/drivers/chromedriver', options=options)
#driver = webdriver.Firefox()
#driver = webdriver.Safari()
driver.maximize_window()

# Wait times
driver.implicitly_wait(4)  # Implicit Wait
xwait = WebDriverWait(driver, 7)  # Explicit Wait

# Declaring Variable
error_detected_flag = 0
item_list = []

url = "https://www.amazon.com/"


def search(keyword):
    global error_detected_flag
    try:
        driver.get(url)

        xwait.until(ec.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
        driver.find_element_by_id("twotabsearchtextbox").send_keys(keyword)

        xwait.until(ec.element_to_be_clickable((By.ID, "nav-search-submit-button")))
        driver.find_element_by_id("nav-search-submit-button").click()

    except NoSuchElementException:
        error_detected_flag = 1
        print("Element not found in search()")
    except ElementClickInterceptedException:
        error_detected_flag = 1
        print("Element not clickable in search()")
    except Exception as e:
        error_detected_flag = 1
        print(e)


def sort_by():
    global error_detected_flag
    try:
        xwait.until(ec.visibility_of_element_located((By.ID, "s-result-sort-select")))  # Click Sort by
        driver.execute_script("arguments[0].click();", driver.find_element_by_id("s-result-sort-select"))
        #driver.find_element_by_id("s-result-sort-select").click()

        xwait.until(ec.element_to_be_clickable((By.ID, "s-result-sort-select_3")))  # Sort by Avg. Customer review
        driver.find_element_by_id("s-result-sort-select_3").click()

        xwait.until(ec.element_to_be_clickable((By.LINK_TEXT, "5 to 7 Years")))  # Sort by "5 to 7 Years"
        driver.find_element_by_link_text("5 to 7 Years").click()

    except NoSuchElementException:
        error_detected_flag = 1
        print("Element not found in sort_by()")
    except ElementClickInterceptedException:
        error_detected_flag = 1
        print("Element not clickable in sort_by()")
    except Exception as e:
        error_detected_flag = 1
        print(e)


def add_to_cart():
    global error_detected_flag
    try:
        for i in range (2,4):
            xwait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div["+str(i)+"]")))
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div["+str(i)+"]").click()

            item_list.append(driver.find_element_by_id("productTitle").text[0:80])
            time.sleep(1)
            xwait.until(ec.element_to_be_clickable((By.ID, "add-to-cart-button")))
            driver.execute_script("arguments[0].click();", driver.find_element_by_id("add-to-cart-button"))

            time.sleep(4)
            driver.back()
        driver.back()

    except NoSuchElementException:
        error_detected_flag = 1
        print("Element not found in add_to_cart()")
    except ElementClickInterceptedException:
        error_detected_flag = 1
        print("Element not clickable in add_to_cart()")
    except Exception as e:
        error_detected_flag = 1
        print(e)


def validate_cart():
    global error_detected_flag
    try:
        driver.refresh()  # to make sure everything is updated in the cart
        xwait.until(ec.visibility_of_element_located((By.ID, "nav-cart-text-container")))
        driver.find_element_by_id("nav-cart-text-container").click()
        for i in range (3,5):
            a = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[3]/div/div[2]/div[4]/div/form/div[2]/div["+str(i)+"]/div[4]/div/div[1]/div/div/div[2]/ul/li[1]/span/a").text[0:80]
            if a in item_list:
                pass
            else:
                print("Incorrect Item in List")

    except NoSuchElementException:
        error_detected_flag = 1
        print("Element not found in validate_cart()")
    except ElementClickInterceptedException:
        error_detected_flag = 1
        print("Element not clickable in validate_cart()()")
    except Exception as e:
        error_detected_flag = 1
        print(e)


search("Teddy Bear")  # Open amazon and add search for "teddy bear"
sort_by()  # Sort the result by avg. customer review and age range
add_to_cart()  # Add the first two items in cart
validate_cart()  # Check if those 2 items are in cart

driver.close()  # Close Window
sys.exit(error_detected_flag)


