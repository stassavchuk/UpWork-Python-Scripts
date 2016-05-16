import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import codecs
import os

BASE_PAGE = "http://findyourvacationhome.com/"
ALL_COUNTRIES_PAGE = BASE_PAGE + "find.php#browse"   # List of Countries
TIME_TO_WAIT = 5    # How much time you are ready to wait for one profile? (in seconds)
OUTPUT_FILENAME = "data.csv"
PHANTOMJS_PATH = r"C:\Users\Stanislav\Desktop\phantomjs-2.0.0-windows\bin\phantomjs.exe"

_browser = None
_output_file = None

def get_set_of_links(url, ANCHOR):
    htmltext = urllib.urlopen(url).read()
    soup = BeautifulSoup(htmltext, "html.parser")

    all_links = soup.findAll("a", href=True)
    links = [BASE_PAGE + link.get("href") for link in all_links if ANCHOR in link.get("href")]

    return set(links)

def get_data():
    sleep_time = 0
    while sleep_time <= TIME_TO_WAIT:
        try:
            htmltext = _browser.page_source
            soup = BeautifulSoup(htmltext, "html.parser")

            name = soup.findAll("h1")[0].contents[0]
            contacts = soup.find_all("h3", text="Contact The Owner")[0].parent.find_all("tr")
            phone = contacts[0].find_all("td")[-1].contents[0]
            email = contacts[2].find_all("a")[0].contents[0]
            website = contacts[3].find_all("td")[-1].contents[0].get("href")
            location = " ".join(re.findall("showAddress.+;", htmltext)[0][12:-2].split('","')[:-1]).replace('"', '')

            return (email, name, location, phone, website)
        except:
            time.sleep(1)
            sleep_time += 1
    return None


def scrap_country(url):
    page = 1
    while True:
        url += "&start=" + str(page)
        profiles = get_set_of_links(url, "property")

        if not profiles:
            break

        for profile in profiles:
            data = None
            try:
                _browser.get(profile)
                data = get_data()
            except:
                pass

            if data:
                write_data(data)

        page += 10

def write_data(data):
    (email, name, location, phone, website) = data

    _output_file.write('"' + email + '","' + name + '","' + location + '","' + phone + '","' + website + '"')
    _output_file.write("\n")

    print_data(data)

def print_data(data):
    (email, name, location, phone, website) = data
    # os.system('cls')  # If you to clean your command prompt

    print "Email:    " + email
    print "Name:     " + name
    print "Location: " + location
    print "Phone:    " + phone
    print "Website:  " + website
    print

if __name__ == "__main__":
    _browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    # _browser = webdriver.Firefox()    # If you want to use Firefox
    _output_file = codecs.open(OUTPUT_FILENAME, "w", encoding="utf-8")

    countries = get_set_of_links(ALL_COUNTRIES_PAGE, "country")
    try:
        for country in countries:
            try:
                scrap_country(country)
            except:
                pass
        _output_file.close()
    except:
        _output_file.close()

    _browser.close()