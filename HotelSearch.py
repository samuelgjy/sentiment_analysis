import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


# accepts hotel name and return the hotel review page url of specified hotel 
def find_hotel_review_page(hotel_name):
    # create a Google search url for the user-specified hotel
    search_string = "%s sg site:www.tripadvisor.com.sg/Hotel_Review" % hotel_name
    urlString = "https://www.google.com/search?&q=%s" % search_string

    # create a fake user agent generator to avoid bot detection
    fake_user_agent = UserAgent()
    headers = {'User-Agent': fake_user_agent.random}

    # search through the response page for the first URL
    response_page = requests.get(urlString, headers=headers)
    soup = BeautifulSoup(response_page.content, "html.parser")
    url_link = str(soup.find('div', class_='egMi0 kCrYT'))

    # return the URL if the hotel is in Singapore, else return None
    if 'Singapore' in url_link:
        url_link = re.search('https://.+?">', url_link)
        url_link = url_link.group().replace('">', '')
        print(url_link)
        return url_link
    else:
        return None


