from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\Ryan\\Desktop\\UDEN201811DATA3\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def news_scrape():
    news = {}
    url_news = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    resps = requests.get(url_news)
    data = resps.json()
    news["news_title"] = data.get('items')[0].get('title')
    news["news_p"] = data.get('items')[0].get('description')
    return news

def featured_img_scrape():
    try:
        browser = init_browser()
        featured_image = {}
        url_feat_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url_feat_img)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        last_part = soup.find('a',{'class':'button fancybox'}).attrs.get('data-fancybox-href')
        the_url = 'https://www.jpl.nasa.gov'+ last_part
        featured_image["url"] = the_url
        return featured_image
    finally:
        browser.quit()

def weather_scrape():
    try:
        browser = init_browser()
        weather = {}
        url_weather = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url_weather)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        tweet = soup.find_all('p',{"class":"TweetTextSize"})
        weather["mars_weather"] = tweet[0].get_text()
        return weather
    finally:
        browser.quit()

def info_scrape():
    df = pd.read_html("http://space-facts.com/mars/")
    dfs= pd.DataFrame.from_records(df[0])
    dfs.columns = ['a','b']
    facts = dfs.to_dict('records')
    return facts

first_part = set()
hemi_url_list=[]

def hemi_scrape():
    try:
        browser = init_browser()
        hemi_url_start = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemi_url_start)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        first_page = soup.find_all('a',{'class':'itemLink product-item'})
        for page in first_page:
            end = page.get('href')
            hemi_url = 'https://astrogeology.usgs.gov' + end
            first_part.add(hemi_url) 


        def title_url_scrape(url):
            try:
                browser = init_browser()
                start = "{}".format(url)
                browser.visit(start)
                soup = BeautifulSoup(browser.html, "html.parser")
                info = soup.find('a',{'target':'_blank'})
                titlex = soup.find('h2',{'class':'title'})
                hemi_dic = {'title':titlex.get_text(), 'url': info.get('href')}
                hemi_url_list.append(hemi_dic)
                return hemi_url_list
            finally:
                browser.quit()
        for url in first_part:
            result = title_url_scrape(url)
            print(result)
        return hemi_url_list
    finally:
        browser.quit()
    
#hemi_scrape()








    

    
