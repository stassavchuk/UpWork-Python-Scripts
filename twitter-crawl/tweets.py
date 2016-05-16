'''Gets data from one Twitter handle and saves it to file.

'''


from selenium import webdriver
import datetime
import codecs
import time

_phantomjs_path = r'C:\Users\Stanislav\PycharmProjects\phantomjs-2.0.0-windows\bin\phantomjs.exe'


def get_tweets(handle, N):
    wd = webdriver.PhantomJS(_phantomjs_path)
    # wd = webdriver.Chrome()
    # time.sleep(1)
    wd.get('https://twitter.com/' + handle)
    tweets = []
    print '@' + handle, 'Browser opened'

    shot = 0
    try:
        while len(tweets) < N and shot < 20:
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(0.5)
            new_tweets = wd.find_elements_by_class_name('tweet-text')

            if len(new_tweets) > len(tweets):
                tweets = new_tweets
                print '@' + handle, len(new_tweets)
                shot = 0
            else:
                shot += 1
                print '@' + handle, len(new_tweets), '(' + str(shot) + ')'
                time.sleep(0.5)
            # if wd.find_element_by_class_name('stream-end').is_displayed():
            #     break
    except:
        error_time = str(datetime.datetime.now().time()).replace(':', '-')
        filename = 'errors/' + '@' + handle + ' ' + error_time
        wd.get_screenshot_as_file(filename + '.png')

        with codecs.open(filename + '.html', "w", "utf-8") as html_file:
            html_file.write(wd.page_source)

    print '@' + handle, 'Browser closed'

    with open('tweets/@' + handle + '.txt', 'w') as f:
        for tweet in tweets[:N]:
            try:
                f.write(tweet.text + '\n')
            except:
                f.write('-'*100 + '\n')

    # wd.close()
    return tweets

if __name__ == '__main__':
    get_tweets('Adele', 1000)
