# Job title as 'Chief Executive Office' , location as 'Florida, USA'
TASK_1_LINK = "https://www.linkedin.com/vsearch/p?title=Chief%20Executive%20Office&openAdvancedForm=true&titleScope=CP&locationType=Y&f_G=us%3A828,us%3A596,us%3A359,us%3A896,us%3A751,us%3A490,us%3A824,us%3A270,us%3A202,us%3A398&rsid=4743187891453932721783&orig=ADVS"
# Education as 'Indian Institute of Technology' , location as 'Delhi'
TASK_2_LINK = "https://www.linkedin.com/vsearch/p?school=Indian%20Institute%20of%20Technology&openAdvancedForm=true&locationType=Y&f_G=in%3A7151,in%3A5343&rsid=4743187891453936745209&orig=ADVS"
# Industry as 'Telecom' , location as 'Moscow'
TASK_3_LINK = "https://www.linkedin.com/vsearch/p?openAdvancedForm=true&locationType=Y&f_G=ru%3A7487,ru%3A7481&f_I=8&rsid=4743187891453936870611&orig=ADVS"

TASK = TASK_1_LINK


from selenium import webdriver
import random
from bs4 import BeautifulSoup
import time
import codecs
import traceback


PHANTOMJS_PATH = r"C:\Users\Stanislav\PycharmProjects\phantomjs-2.0.0-windows\bin\phantomjs.exe"

# LinkedIn Account
USER_LOGIN = ""
USER_PASSWORD = ""

BASE_PAGE = "https://www.linkedin.com"
LOGIN_PAGE = BASE_PAGE + "/uas/login"
SEARCH_PAGE = BASE_PAGE + "/vsearch/f"

# Output file
CSV = "output.csv"

# How many first profiles data would you like to grab?
MAX_COUNT = 100

# Time limits
LOGIN_TIME_WAIT = 20
GETTING_PAGE_TIME_WAIT = 10
EMAIL_TIME = 4
GETTING_PROFILE_TIME_WAIT = 30

# If you want to simulate human actions, click to the links with different frequency
HUMAN_SIMULATE = False


def login(browser, user_name, password):
    browser.get(LOGIN_PAGE)
    done_time = 0
    print "Logging in..."
    while done_time <= LOGIN_TIME_WAIT:
        try:
            browser.find_element_by_id("session_key-login").send_keys(USER_LOGIN)
            browser.find_element_by_id("session_password-login").send_keys(USER_PASSWORD)
            browser.find_element_by_id("btn-primary").submit()
            while done_time <= LOGIN_TIME_WAIT:
                if browser.current_url != LOGIN_PAGE and browser.current_url != LOGIN_PAGE + "-submit":
                    # if "Sing-In Verification" in browser.find_element("body").text:
                    print "We are logged in."
                    return True
                else:
                    time.sleep(1)
                    done_time += 1
        except:
            time.sleep(1)
            done_time += 1
    print "I can't log in."
    return False


def find_links_on_page(browser):
    done_time = 0
    print "Processing page..."
    while done_time <= GETTING_PAGE_TIME_WAIT:
        try:
            htmltext = browser.find_element_by_id("results").get_attribute('innerHTML')
            soup = BeautifulSoup(htmltext, "html.parser")
            all_links = soup.findAll("a", {"class": "title main-headline"})
            links = [link.get("href") for link in all_links]
            print "Found " + str(len(links)) + " profiles."
            htmltext = browser.find_element_by_id("results-pagination").get_attribute("innerHTML")
            soup = BeautifulSoup(htmltext, "html.parser")
            break
        except:
            time.sleep(1)
            done_time += 1
    if done_time > GETTING_PAGE_TIME_WAIT:
        print "Loading takes to much time"
        return False
    next = None
    try:
        next = BASE_PAGE + soup.find_all("li", {"class": "next"})[0].find_all("a")[0].get("href")
    except:
        pass

    return (next, links)


def scrap_profile(browser, url):
    browser.get(url)
    print "\nProcessing new profile..."

    name = ""
    title = ""
    company_name = ""
    adress = ""
    country = ""
    email = ""

    done_time = 0
    while done_time <= GETTING_PROFILE_TIME_WAIT:
        try:
            name = browser.find_element_by_id("name").text
            print "Name: " + name
            break
        except:
            time.sleep(1)
            done_time += 1
    if done_time > GETTING_PROFILE_TIME_WAIT:
        print "Profile is loading to slow..."
        return False
    try:
        title = browser.find_element_by_id("headline").text
        print "Title: " + title
    except:
        pass
    try:
        company_name = browser.find_element_by_id("overview-summary-current").text.replace("Current", "").replace("\n", "")
        print "Company: " + company_name
    except:
        pass
    try:
        htmltext = browser.find_element_by_id("location").get_attribute('innerHTML')
        soup = BeautifulSoup(htmltext, "html.parser")
        location = soup.find_all("a", {"name": "location"})[0].text.split(',')
        if len(location) > 1:
            adress = location[0]
            print "Adress: " + adress
        country = location[-1]
        print "Country: " + country
    except:
        pass
    try:
        network = browser.find_element_by_class_name("fp-degree-icon").text
        if network == "1st":
            email = ""
            elem = browser.find_elements_by_xpath("//*[contains(text(), 'Contact Info')]")[0]
            elem.click()
            d_time = 0
            if elem:
                while d_time < EMAIL_TIME:
                    try:
                        email = browser.find_element_by_id("relationship-email-item-0").text
                    except:
                        pass
                    if email:
                        break
                    else:
                        time.sleep(1)
                        d_time += 1
            print "Email: " + email
    except:
        pass
    try:
        url = browser.current_url.split("?")[0]
        print "url: " + url
    except:
        pass

    return (name, title, company_name, adress, country, email, url)


def write_to_csv(profile_data, csv_document):
    (name, title, company_name, adress, country, email, url) = profile_data
    csv_document.write(
        '"' + name + '", ' +
        '"' + title + '", ' +
        '"' + company_name + '", ' +
        '"' + adress + '", ' +
        '"' + country + '", ' +
        '"' + email + '", ' +
        '"' + url + '"\n'
    )


def main(browser, csv_document, task):
    if not login(browser, USER_LOGIN, USER_PASSWORD):
        return
    browser.get(task)
    count = 0
    page = 0
    while count <= MAX_COUNT:
        data = find_links_on_page(browser)
        page += 1
        if data:
            (next, links) = data
        for link in links:
            profile_data = scrap_profile(browser, link)
            if profile_data:
                write_to_csv(profile_data, csv_document)
                count += 1
            else:
                pass
                # Write to Error
            if HUMAN_SIMULATE:
                time.sleep(random.randrange(3, 7, 0.1))
        if next:
            browser.get(next)
        else:
            break


if __name__ == "__main__":
    browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    csv_document = codecs.open(CSV, "a", encoding="utf-8")

    try:
        main(browser, csv_document, TASK)
    except:
        browser.save_screenshot("1.png")
        csv_document.close()
        browser.close()
        traceback.print_stack()


    csv_document.close()
    browser.close()