from scraper import Scraper

if __name__ == "__main__":
    links = []
    doc = open("URLs.csv", "r").read()
    try:
        for line in doc.split("\n"):
            l = line.split(";")[-2]
            links.append("https://www.sec.gov/Archives/" + l + "-index.htm")
    except:
        pass

    errors = open("errors.txt", "w")
    try:
        for index, link in enumerate(links[:1000]):
            # try:
            print index, Scraper.scrap(link)
            print
            # except Exception as ex:
            #     errors.write(str(index) + ":  " + str(link) + "\n")
    finally:
        errors.close()