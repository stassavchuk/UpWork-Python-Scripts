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

