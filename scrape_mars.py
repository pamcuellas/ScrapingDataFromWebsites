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

# In[2]:

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    json_data = {}

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
    # print(link_latest_news)

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

    # Get the paragraph list
    lst_p = soup.find("div", class_="wysiwyg_content")
    # Get the first paragraph
    last_p = lst_p.find_all("p")[0]
    last_p = last_p.text

    json_data["last_title"] = last_title
    json_data["last_p"] = last_p
    # ### JPL Mars Space Images - Featured Image

    # In[5]:

    # Go to the news page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # In[6]:


    # Use splinter to navigate the site and find the image url for the current Featured 
    # Mars Image and assign the url string to a variable called featured_image_url.
    # Get the Image URL
    carousel_item = soup.find('article', class_="carousel_item")['style']
    featured_image_url = 'https://www.jpl.nasa.gov' + carousel_item.split("'")[1]

    # print("The URL is {}".format(featured_image_url))

    json_data["featured_image_url"] = featured_image_url

    # ### Mars Weather

    # In[7]:

    # Visit the Mars Weather twitter account here (https://twitter.com/marswxreport?lang=en) and scrape the latest 
    # Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Remove tag a from tag p (Mars Weather).
    for a in soup.find_all("a", {'class':'twitter-timeline-link u-hidden'}): 
        a.decompose()

    # Get the Mars Weather
    ol = soup.find("ol", class_="stream-items js-navigable-stream")
    li = ol.find_all("li")[0]
    div = li.find("div", class_="js-tweet-text-container")
    mars_weather = div.find("p").text + "."
    json_data["mars_weather"] = mars_weather 

    # ### Mars Facts

    # In[8]:

    # Visit the Mars Facts webpage here (https://space-facts.com/mars/) and use Pandas to scrape 
    # the table containing facts about the planet including Diameter, Mass, etc.
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.rename(columns={0:"Description",1:"Value"}, inplace=True)

    # In[9]:

    # Use Pandas to convert the data to a HTML table string.
    html_temp = df.to_html(index=False, escape=False, justify="left", classes="table table-striped table-bordered table-sm")

    # Change the first column from td to th.
    html_table = ""
    for row in html_temp.split("<tr>"): 
        row = row.replace("<td>","<th>",1)
        row = row.replace("</td>","</th>",1)
        html_table = html_table + "<tr>" + row
    html_table = html_table.replace("<tr>","",1)

    json_data["html_table"] = html_table

    # ### Mars Hemispheres

    # In[10]:

    # Visit the USGS Astrogeology site here (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar"s hemispheres.
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_image_urls =[]
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get text links to click
    items = soup.find_all("div", class_="description")
    lst_text =[]
    for item in items:
        lst_text.append(item.h3.text)

    # Looping to click 
    for i in range( len(lst_text) ):
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        browser.click_link_by_partial_text(lst_text[i])

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        # Get the image URL
        tmp_img_url = soup.find('img',class_="wide-image")["src"]
        img_url = "https://astrogeology.usgs.gov" + tmp_img_url

        # Get the title
        title = soup.title.text
        title = title.split("|")[0]
        title = title.replace("Enhanced","")
        title = title.strip()
        # Append the dictionary with the image url string and the hemisphere title to a list. 
        hemisphere_image_urls.append({"title":title, "img_url": img_url})     

    # Add list of images URL and title to json_data 
    json_data["hemisphere_image_urls"] = hemisphere_image_urls

    # Close the browser window
    browser.quit()

    return json_data


