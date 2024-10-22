import time
import requests
#import undetected_chromedriver as uc
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time
import re
import xml.etree.ElementTree as ET
import feedparser
from dateutil import parser

def new_feed_input(today):
    # Get user input for the URL
    global pub_date
    rss_url = "https://newalbumreleases.net/feed/"
    while True:
        try:

            #options= ChromiumOptions().headless(False)
            options = ChromiumOptions().auto_port()
            drive= ChromiumPage(options)
            drive.listen.start()
            drive.get(rss_url)
            time.sleep(30)
            drive._wait_loaded(30)
            i = drive.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
            #i = drive.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=8c5ebae438db7f9f')
            if i:
                e = i('.mark')
                e.click()

            drive._wait_loaded(30)
            #time.sleep(5)
            htmls = drive.html
            parsed= feedparser.parse(htmls)
            #print(htmls)
            rss_content = parsed['feed']['summary']
            #print(rss_content)
            drive.listen.clear()
            drive.quit()
            links = []

            # Extract the XML content (make sure it's complete and well-formed)
            soup = BeautifulSoup(rss_content, 'lxml')
            pre_tag = soup.find('pre')
            xml_data = pre_tag.text  # This should contain your XML data
            break
        #except (xml_data== "") or (xml_data== None) or AttributeError:
        except (UnboundLocalError,AttributeError):
            #driver.quit()
            print("Attempt failed..Retrying")
            new_feed_input(today)
    #print(rss_content)
        # Parse the RSS feed content using BeautifulSoup


    # Now parse the XML data with BeautifulSoup using 'xml' parser
    soup_xml = BeautifulSoup(xml_data, 'xml')

    # Your further processing of the XML goes here...
    # For example, finding the <rss> tag
    rss_tag = soup_xml.find('rss')
    rss_string = str(rss_tag)
    root = ET.fromstring(rss_string)
    items = root.findall('.//item')
    for item in items:
        #print(item.find('title').text)
        #print(item.find('link').text)
        #print(item.find('pubDate').text)
        link = item.find('link').text
        date_string = item.find('pubDate').text.strip()
        #print(date_string)
                #pub_date = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        #pub_date = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        pub_date = parser.parse(date_string)
        pub_date = pub_date.astimezone(timezone.utc).date()
        formatted_date = pub_date.strftime("%Y-%m-%d")


            # Check if the entry date is today and add the link to the list if it is
        if str(formatted_date) == str(today):
            links.append(link)
    #print(links)
    return links,str(pub_date)

def page_view(url):
    while True:
        try:
            #options= ChromiumOptions().headless(False)
            options = ChromiumOptions().auto_port()
            options.set_argument('--no-sandbox')
            #options = ChromiumOptions().headless(True)
            drive= ChromiumPage(options)
            drive.listen.start()
            drive.get(url)
            time.sleep(10)
            htmls = drive.html
            parsed= feedparser.parse(htmls)
            #print(parsed['feed'])
            rss_content = parsed['feed']['summary']
            #if rss_content:
                #print(rss_content)
            #else:
                #print("None")
            i = drive.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
            if i:
                e = i('.mark')
                e.click()
            #time.sleep(10)
            #resp = driver.listen.wait()
            #rss_content = resp.response.body
            #print(rss_content)
            drive.listen.clear()
            drive.quit()

            break
        #except (rss_content== "") or (rss_content== None):
        except UnboundLocalError:
            #driver.quit()
            print("Attempt failed..Retrying")
            page_view(url)
    #print(rss_content)
        # Parse the RSS feed content using BeautifulSoup
    links=[]

    # Extract the XML content (make sure it's complete and well-formed)
    #soup = BeautifulSoup(rss_content, 'lxml')
    #pre_tag = soup.find('pre')
    #xml_data = pre_tag.text  # This should contain your XML data

    # Now parse the XML data with BeautifulSoup using 'xml' parser
    soup_xml = BeautifulSoup(rss_content, 'html.parser')
    #print(soup_xml)
    return soup_xml
def page_view2(url):
    while True:
        try:
            #options= ChromiumOptions().headless(False)
            options = ChromiumOptions().auto_port()#.headless(True)
            options.set_argument('--no-sandbox')
            #options = ChromiumOptions().headless(True)
            drive= ChromiumPage(options)
            drive.listen.start()
            drive.get(url)
            i = drive.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
            if i:
                e = i('.mark')
                e.click()
            htmls = drive.html
            time.sleep(10)  # orginally set to 10
            #print(htmls)
            #return
            parsed= feedparser.parse(htmls)
            #print(parsed)
            #print(parsed['feed'])
            rss_content = parsed['feed']
            #if rss_content:
                #print(rss_content)
            #else:
                #print("None")
            #time.sleep(10)
            #resp = driver.listen.wait()
            #rss_content = resp.response.body
            #print(rss_content)
            drive.listen.clear()
            drive.quit()

            break
        #except (rss_content== "") or (rss_content== None):
        except UnboundLocalError:
            #driver.quit()
            print("Attempt failed..Retrying")
            page_view2(url)
    #print(rss_content)
        # Parse the RSS feed content using BeautifulSoup
    links=[]

    # Extract the XML content (make sure it's complete and well-formed)
    #soup = BeautifulSoup(rss_content, 'lxml')
    #pre_tag = soup.find('pre')
    #xml_data = pre_tag.text  # This should contain your XML data
    #root = ET.fromstring(htmls)

    # Now parse the XML data with BeautifulSoup using 'xml' parser
    soup_xml = BeautifulSoup(htmls, 'html.parser')
    #soup_xml=BeautifulSoup(ET.tostring(root),"xml")
    #print(soup_xml)
    return soup_xml

if __name__ == "__main__":
    #today = datetime.now(timezone.utc).date()
    #print(new_feed_input(today))
    #page_view("https://newalbumreleases.net/209779/skerryvore-tempus-2024/")
    soup1=page_view2("https://musicstax.com/search?q=Bryce+Dessner++Lullaby+for+Jacques+et+Brune+")
    track_element = str(soup1.find(class_='song-image search-image'))
    #print(track_element)
    match = track_element.split('"')[5]
    track_url = "https://musicstax.com" + match
    soup2 = page_view2(track_url)
    print(soup2)
    site = soup2.find_all(class_='song-bar-statistic-number')
    # print(site)
    dance = str(site[2])
    energy = str(site[1])
    release_date_value = None  # Initialize the variable
    #release_date_label = soup2.find('div', attrs={'data-cy': 'meta-Release+Date-label'})
    release_date_label = soup2.find_all(class_='song-meta-item-stat')

    if release_date_label:
        release_date_value = release_date_label[3]

    date = release_date_value.text if release_date_value else "None"
    try:
        syear = int(date[-4:])
        print(syear)
    except ValueError:
        print("Unknown year")
        syear = "None"