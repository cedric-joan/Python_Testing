from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# connexion app
browser = webdriver.Chrome(chrome_options)
browser.get("http://127.0.0.1:5000/")
element_h1 = browser.find_element(By.TAG_NAME, value="h1").text
assert element_h1 == "Welcome to the GUDLFT Registration Portal!"

# login user
email = browser.find_element(By.NAME, value='email')
email.send_keys('john@simplylift.co')
email.send_keys(Keys.ENTER)
assert browser.current_url == "http://127.0.0.1:5000/show-summary"
element_h3 = browser.find_element(By.TAG_NAME, value='h3').text
assert element_h3 == "New Competitions:"

# user chooses a competition and click on book in order to purchase places
book_link = browser.find_element(By.XPATH, value="/html/body/table[1]/tbody/tr[1]/td[4]/a")
book_link.click()
assert browser.current_url == "http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift"

# user books places
select_places = browser.find_element(By.NAME, value='places')
select_places.send_keys('4')
select_places.send_keys(Keys.ENTER)

display_number_of_places = browser.find_element(By.XPATH, value='/html/body/p').text
assert '9' in display_number_of_places

# logout user
logout = browser.find_element(By.XPATH, value='/html/body/nav/div/a')
logout.click()
assert browser.current_url == "http://127.0.0.1:5000/logout"