from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import xlsxwriter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

##############################
# opening to website
##############################
driver= webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
#print('01010101010101')
sleep(2)

##############################
# import username and password
##############################

#credential = open('E:\\own\\banking\\udacity\\data\\pro\\test\\credentials.txt')
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
sleep(2)

##############################
# login
##############################

#email_field = driver.find_element_by_xpath('//*[@id="username"]')
#WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
email_field = driver.find_element_by_id('username')
password_field = driver.find_element_by_id('password')
email_field.send_keys(username)
password_field.send_keys(password)
#print('21212121212')
sleep(25)

#signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
#WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')))
#signin_field.click()

##############################
# searching
##############################

#print('00000000000')
#search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
#WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@class="search-global-typeahead__input always-show-placeholder"]')))

search_word = line[2]
search_field = driver.find_element_by_xpath('//*[@id="global-nav-typeahead"]/input')
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
#print('- 222222222222')                     #
sleep(2)
search_field.send_keys(search_word)       #
search_field.send_keys(Keys.RETURN)
#print('444444444444')
sleep(3)

##############################
# press button people
##############################
# //*[@id="search-reusables__filters-bar"]/ul/li[1]/button
# //*[@id="main"]/div/div/div[1]/div[2]/a
people_button = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/a')
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/div[2]/a')))
people_button.send_keys(Keys.RETURN)

##############################
# press button people
##############################


sleep(3)

##############################
# get urls for one page
##############################
def GetURL():

    #print('0000000')
    page_source = BeautifulSoup(driver.page_source)
    #print('11111111111')
    profiles = page_source.find_all("span",{"class":"entity-result__title-text t-16"})
    all_profile_URL = []
    for profile in profiles:
        a = profile.select("a")
        for i in a :
            profile_URL = i.get('href')
            if profile_URL not in all_profile_URL:
                all_profile_URL.append(profile_URL)
                print(profile_URL)

    return all_profile_URL

print('11111111111')

##############################
# get urls for all pages
##############################
page_source = BeautifulSoup(driver.page_source)
num_of_pages = int(line[3])
url_all_page = []
with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()

    for i in range(num_of_pages):

        url_current_page = GetURL()
        for x in url_current_page:
            try:
                writer.writerow({headers[0]:x})
            except:
                pass
        sleep(2)
        #print('222222222222')
        #scroll down to the end of the page
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        #print('3333333333')
        next_button = driver.find_element_by_class_name('artdeco-pagination__button--next')
        #print('44444444444')
        url_all_page = url_all_page + url_current_page
        next_button.click()
        sleep(2)
        print(len(url_all_page))

print('\n-----------Succesfully get all url pages------\n')
##############################
# get info from urls for all pages
##############################

with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location','Current Cumppany', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in url_all_page:
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        try:
            name = page_source.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters
            title = page_source.find('div', class_='text-body-medium break-words').get_text().strip()
            location = page_source.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters
            current_cumppany = page_source.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline').get_text().strip()
            writer.writerow({headers[0]:name, headers[1]:title, headers[2]:location, headers[3]:current_cumppany, headers[4]:linkedin_URL})
        except:
            pass


print('\n-----------Succesfully get all info from url pages------\n')
