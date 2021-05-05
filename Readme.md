## Web scraping real estate information from newspaper(online) ads using Python and Selenium

This assumes you have Selenium Chromedriver installed and you know, of course, the startpage for scraping.  
The path to Chromedriver can be specified using the PATH in realestate.py.  
The startpage is specified in the variable of the same name in realestate.py  
Sleep commands during scraping are intended to make the behavior more similar to human browsing, however they also increase runtime.

Scripts:
+ realestate - scraping real estate data with Selenium
+ process_data - processing the raw scraped data

Output:
+ realestate.csv - raw scraped data; columns are separated by "|"
+ realestate-clean.csv - processed data; columns are separated by ";"
