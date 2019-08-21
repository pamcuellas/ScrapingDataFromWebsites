#!/usr/bin/env python
# coding: utf-8

# # <h1 style="color: purple;">Step 1 - Scraping</h1>

# ### NASA Mars News

# In[1]:


# Import Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.common.exceptions import ElementNotVisibleException
import json

# In[2]:

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    json_data = []

    # Scrape the NASA Mars News Site here (https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
    # and collect the LATEST News TITLE and PARAGRAPH Text. Assign the text to variables that you can reference later.
    # Example:

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the list of news 
    ul_list_news = soup.find("ul", class_="item_list")
    # Get the last news
    li_last_news = ul_list_news.find_all("li")[0]
    # Get the link for the last news.
    link_latest_news = li_last_news.find("a")["href"]
    print(link_latest_news)


    # In[3]:

    
    # Go to the news page
    url = url.replace("/news","",1) + link_latest_news
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    # In[4]:


    # Get the title
    last_title = soup.find("h1", class_="article_title")
    last_title = last_title.text
    last_title = last_title.replace("'","")

    # Get the paragraph list
    lst_p = soup.find("div", class_="wysiwyg_content")
    # Get the first paragraph
    last_p = lst_p.find_all("p")[0]
    last_p = last_p.text
    last_p = last_p.replace("'","")

    json_data.append({"last_title":last_title, "last_p":last_p})

    # ### JPL Mars Space Images - Featured Image

    # In[5]:


    # Visit the url for JPL Featured Space Image here ==> https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.
    # Go to the news page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    # In[6]:


    # Get the figure ID.
    carousel_item = soup.find("article", class_="carousel_item")
    footer = carousel_item.find("footer")
    id_fig = footer.find("a")["data-link"]
    id_fig = id_fig.split("=")[1]

    # Use splinter to navigate the site and find the image url for the current Featured 
    # Mars Image and assign the url string to a variable called featured_image_url.
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/" + id_fig + "_hires.jpg"

    print("The URL is {}".format(featured_image_url))

    json_data.append({"featured_image_url":featured_image_url})

    # ### Mars Weather

    # In[7]:


    # Visit the Mars Weather twitter account here (https://twitter.com/marswxreport?lang=en) and scrape the latest 
    # Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    ol = soup.find("ol", class_="stream-items js-navigable-stream")
    li = ol.find_all("li")[0]
    div = li.find("div", class_="js-tweet-text-container")
    mars_weather = div.find("p").text

    json_data.append({"mars_weather":mars_weather})

    # ### Mars Facts

    # In[8]:


    # Visit the Mars Facts webpage here (https://space-facts.com/mars/) and use Pandas to scrape 
    # the table containing facts about the planet including Diameter, Mass, etc.
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.rename(columns={0:"info",1:"value"}, inplace=True)
    df.set_index("info", inplace=True)

    # In[9]:


    # Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html()
    html_table = html_table.replace("\n", "")

    json_data.append({"html_table":html_table})

    # ### Mars Hemispheres

    # In[10]:


    # Visit the USGS Astrogeology site here (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar"s hemispheres.
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    url_lst =[]
    lst = soup.find("div", class_="collapsible results")
    lst_a = lst.find_all("div", class_="item")

    for item in lst_a:
        lala = item.find("div", class_="description")
        url_lst.append("https://astrogeology.usgs.gov" +  lala.find("a")["href"])


    # In[11]:


    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    hemisphere_image_urls =[]
    for url_fig in url_lst:
        browser.visit(url_fig)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing
        # the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
        html_block = soup.find("div", class_="downloads")
        img_url = "https://astrogeology.usgs.gov" + html_block.find("img")["src"]
        title = soup.title.text
        title = title.split("|")[0]
        title = title.replace("Enhanced","")

        # Append the dictionary with the image url string and the hemisphere title to a list. 
        # This list will contain one dictionary for each hemisphere.
        hemisphere_image_urls.append({"title":title, "img_url": img_url})     
        json_data.append({"hemisphere_image_urls":hemisphere_image_urls})
        browser.quit()

        print(json_data)
        print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(json.dumps(json_data)) 


        return json.dumps(json_data)


