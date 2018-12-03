
# coding: utf-8

# In[64]:


#Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
import time


# In[65]:


from splinter import Browser
from urllib.parse import urlsplit
from splinter.exceptions import ElementDoesNotExist


# In[66]:


#Set up windows path
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[67]:


#nasa URL
url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[68]:


# Scrape page into soup
html = browser.html
soup = bs(html, 'html.parser')


# In[69]:


#pull title and paragraph
news_title = soup.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


# In[70]:


#Visit the url for JPL Featured Space Image
jpl_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)

# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(jpl_url))
print(base_url)


# In[71]:


#Establish xpath
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"


# In[72]:


#Use splinter to get full res image
results = browser.find_by_xpath(xpath)
image = results[0]
image.click()


# In[73]:


#Retreive image urls
html_image = browser.html
soup = bs(html_image, "html.parser")
image_url = soup.find("img", class_="fancybox-image")["src"]
full_image_url = base_url + image_url
print(full_image_url)


# In[74]:


#get mars weather's latest tweet from the website
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[75]:


#scrape
html_weather = browser.html
soup = bs(html_weather, "html.parser")
#temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# In[76]:


#mars facts url
mars_facts = "https://space-facts.com/mars/"


# In[77]:


#retreive table
table = pd.read_html(mars_facts)
table[0]


# In[78]:


#sort by fact and value
mars_df = table[0]
mars_df.columns = ["Fact", "Value"]
mars_df.set_index(["Fact"])


# In[79]:


#Convert to HTML string
mars_html = mars_df.to_html()
mars_html = mars_df.replace("\n", "")
mars_html


# In[80]:


#Mars Hempisphere URL
hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_url)


# In[81]:


#soup
html_hemis = browser.html
soup_hemis = bs(html_hemis, 'html.parser')


# In[89]:


hemis_links = soup_hemis.find_all('a', class_="itemLink product-item")


# In[83]:


print(hemis_links)


# In[84]:


#Verify number of image links
links = browser.find_by_css("a.product-item")
number = len(links)
number


# In[85]:


#create table
hemisphere_images = []


# In[87]:


#Python code with loop
for i in range (number):
    hemisphere = {}
    i = i + 1
    
    print(i)
    try:
        browser.find_by_css('a.product-item')[i].click()
        
    except:
        continue
    
    hemi_href = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = hemi_href['href']
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_images.append(hemisphere)
    print(i)
    browser.back()


# In[88]:


#flat url
hemisphere_images

