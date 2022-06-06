#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC



web = 'https://www.amazon.com'
driver_path = 'C:/Users/Admin/Desktop/To_Do_Automate/Mon/chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('--headless')

driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.get(web)

driver.implicitly_wait(5)
keyword = "wireless charger"
search = driver.find_element(by=By.XPATH, value='//*[(@id = "twotabsearchtextbox")]')
search.send_keys(keyword)
# click search button
search_button = driver.find_element(by=By.ID, value='nav-search-submit-button')
search_button.click()

driver.implicitly_wait(5)

product_asin = []
product_name = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
for item in items:
    # find name
    name = item.find_element(by=By.XPATH, value='.//span[@class="a-size-medium a-color-base a-text-normal"]')
    product_name.append(name.text)

    # find ASIN number 
    data_asin = item.get_attribute("data-asin")
    product_asin.append(data_asin)

    # find price
    whole_price = item.find_elements(by=By.XPATH, value='.//span[@class="a-price-whole"]')
    fraction_price = item.find_elements(by=By.XPATH, value='.//span[@class="a-price-fraction"]')
    
    if whole_price != [] and fraction_price != []:
        price = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        price = 0
    product_price.append(price)

    # find ratings box
    ratings_box = item.find_elements(by=By.XPATH, value='.//div[@class="a-row a-size-small"]/span')

    # find ratings and ratings_num
    if ratings_box != []:
        ratings = ratings_box[0].get_attribute('aria-label')
        ratings_num = ratings_box[1].get_attribute('aria-label')
    else:
        ratings, ratings_num = 0, 0
    
    product_ratings.append(ratings)
    product_ratings_num.append(str(ratings_num))
    
driver.quit()

# to check data scraped
print(product_name)
print(product_asin)
print(product_price)
print(product_ratings)
print(product_ratings_num)


# In[12]:


data = {"Product Name": product_name, "Unique ID":product_asin, "Product Price":product_price, "Product Ratings":product_ratings, "Rating Numbers":product_ratings_num}


# In[13]:


df = pd.DataFrame(data)
df


# In[14]:


df.to_csv('Amazon_details.csv')
df.to_csv('Amazon_data.xlsx')


# In[15]:


import sqlite3


# In[16]:


conn = sqlite3.connect('test_database')
c = conn.cursor()


# In[17]:


c.execute('CREATE TABLE IF NOT EXISTS products (product_name text, product_asin  varchar, product_price  real, product_ratings  varchar, product_ratings_num real)')
conn.commit()


# In[ ]:





# In[ ]:





# In[18]:


df.to_sql('Amazons_database')


# In[ ]:




