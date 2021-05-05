from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'

# initialize webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(PATH, chrome_options=options)

sources = {} # source: startpage
sources["detoatepentrutoti"] = [ "https://www.detoatepentrutoti.ro/cautare?domeniu=Imobiliare&categoria=Imobile&rubrica=&tranzactie=1&judet=31&localitate=&sortare_data=desc&keyword=cuvant+cheie&filtru=aplicat&startPage=", "realestate.csv"]


startpage = "https://www.detoatepentrutoti.ro/cautare?domeniu=Imobiliare&categoria=Imobile&rubrica=&tranzactie=1&judet=31&localitate=&sortare_data=desc&keyword=cuvant+cheie&filtru=aplicat&startPage="
data  = {}
has_page = True
outfile = open("realestate.csv", "w", encoding = "utf8") # output file for raw scraped data
count = 0

try:
    while True:
        # get page
        driver.get(startpage)
        print(driver.title)
        time.sleep(5)
        
        articles = driver.find_elements_by_class_name("anuntList")
        # print("Articles: ")
        # print(articles)
        
        for article in articles: # for test purposes -> articles[:1]: or ->articles[:5]:
            price = article.find_element_by_class_name("anuntListRightPret")
            print(price.text)
            img = article.find_element_by_class_name("anuntListImg")
            link = img.get_attribute("href")
            # print(link)
            dates = article.find_element_by_class_name("anuntListRightAdded")
            # print(dates.text)
            
            # store article information in dictionary
            data[count] = [link, price.text, dates.text]
            count += 1
            time.sleep(5)
        
        # get next page
        nextpage = driver.find_element_by_class_name("last")
        if nextpage is not None:
            pagelink = nextpage.get_attribute("href")
            print(pagelink)
            if pagelink is not None:
                startpage = pagelink
            else: 
                has_page = False
        else:
            has_page = False
        
        if not has_page:
            break
    
    
    # after the main pages were read, browse through the detail pages
    for elem in data:
        # load details page using the stored links
        driver.get(data[elem][0])
        print(driver.title)
        time.sleep(3)
        details = driver.find_element_by_class_name("paidDetailOptions")
        # print(details.text)
        data[elem].append(details.text)
        line = "|".join(data[elem])
        outfile.write(line + "\n")
    
finally:
    driver.quit()
    # close output file
    outfile.close()


