
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


# In[2]:


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[17]:


# Function to scrape mars weather from a whole bunch of sources
def scrape():
    
    #Initialize browser
    browser = init_browser()
    
    #set blank dictionary for eventual completion for website
    mars = {}
    
    #scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #get current news title and paragraph
    news_titles = soup.find_all('div', class_="content_title")
    mars["news_title"] = news_titles[0].find('a').text
    news_p = soup.find_all('div', class_="article_teaser_body")
    mars["latest_news_p"] = news_p[0].text
    
    #visit the JPL website
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    
    #extract the final image URL after a bunch of clicks
    browser.find_by_id('full_image').click()
    time.sleep(5)
    
    browser.find_link_by_partial_text('more info').click()
    
    #scrape page info with soup
    html_JPL = browser.html
    soup_jpl = BeautifulSoup(html_JPL, 'html.parser')
    
    #get the URL and put into dictionary
    feature_image_url = browser.find_link_by_partial_href('largesize')['href']
    mars["feature_image_url"] = feature_image_url
    
    #now to scrape the Mars twitter feed...
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html_weather = browser.html
    soup_weather = BeautifulSoup(html_weather, 'html.parser')
    
    #find the latest tweet and put it into the Mars dictionary
    weather_p = soup_weather.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars["weather"] = weather_p[0].text
    
    #Now to get the Mars facts...
    facts_url = 'http://space-facts.com/mars'
    mars_table = pd.read_html(facts_url, flavor = 'html5lib')
    
    #get the html table into pandas, clean it up, and spit into the mars dictionary
    mars_df = mars_table[0]
    mars_df.columns = ['Description', 'Value']
    mars_html = mars_df.to_html(index=False)
    mars_html = mars_html.replace('\n','')
    mars['fact_table'] = mars_html
    
    #go to the hemisphere website for pictures/links
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html_hemis = browser.html
    soup_hemis = BeautifulSoup(html_hemis, 'html.parser')
    
    #find the number of links to scroll through
    links = browser.find_by_css("a.product-item")
    number = len(links)
    
    #empty list for the hemisphere image links
    hemisphere_image_urls = []
    
     #run a loop to find the URLs needed.  Because the a.product-item it duplicated, there is a "try" in the code in case of error.
    for i in range (number):
        hemisphere = {}
        i = i + 1
    
        try:
            browser.find_by_css('a.product-item')[i].click()
        
        except:
            continue
    
        hemi_href = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = hemi_href['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        
        #now put image links into the mars dictionary
    mars["hemisphere_urls"] = hemisphere_image_urls
    
    #now to get out of the browser
    browser.quit()
    return mars


# In[15]:




