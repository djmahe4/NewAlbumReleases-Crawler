from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
import time
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import timezone

def new_feed_input(today):
    # Get user input for the URL
    global pub_date
    rss_url = "https://newalbumreleases.net/feed/"
    while True:
        try:

            options= ChromiumOptions().auto_port()
            #options.set_argument('--no-sandbox')
            #drive= ChromiumPage(options)
            drive = ChromiumPage(addr_or_opts=options)
            drive.listen.start()
            drive.get(rss_url)
            #time.sleep(30)
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
def org(today):
    # Get user input for the URL
    global pub_date
    rss_url = "https://newalbumreleases.net/feed/"
    while True:
        try:

            options= ChromiumOptions().headless(False)
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
today = datetime.now().date()
links, lastitem = org(today)
print(links)
print(lastitem)



#page.get('https://newalbumreleases.net/feed/')
#time.sleep(1)