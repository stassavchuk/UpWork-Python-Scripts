# UpWork Python Scripts
### A repository for some of solutions to problems that I worked with on UpWork.

#### FindYourVacationHome
Is a crawler for web site **findyourvacationhome.com**. I used here Python 2.7, BeautifulSoup library and Selenium Web Driver with PhantomJS as a browser.

#### sec.gov
www.sec.gov is a website that contains a lot of data.
The aim of project to create a python script to scrape all of the information from pages like this: https://www.sec.gov/Archives/edgar/data/1000180/000110465915071945/0001104659-15-071945-index.htm
This is the Python module that takes the URL/path as an input, and return the information in a tuple.

It gets this information from each page:

- Filing Date, Filing Date Changed, Accepted, Documents
- Name (Filer), IRS No., State of Incorp., Fiscal Year End, Type, Act, File No., Film No., SIC
- Seq, Description, Document, URL, Type, Size

#### LoadingInputAutomatically

Achieves the following:
1. Check every x minutes if there is a new file in a folder.
2. If there is a new file that can be of data type txt, csv, xml, json or xls, load (only) this new file safely. The program should be able to deal with all of them.
3. The file will always contain the following pieces of information for multiple individuals:
    - A personal name (string)
    - A university name (string)
    - A subject name (string)
    - A degree type (string)
    - A grade (German style: float between 0.7 and 4.0)
    - A year (integer)
4. Once you have loaded this data write it into a txt file.
5. Let python send this file in an email with some text to an email address of choice.

#### ip-whois

Provides data about IP addresses:
- ISP Name
- Country
- BGP AS Number
- Reverse DNS Lookup
- Coordinates (x, y)
- If ip is private according to RFC 1918

#### twitter-crawl

Takes 1000 first tweets of person and saves it into files.
The goal of project was to collect tweets of a lot of people.

#### plotly

Builds plots using Plot.ly service