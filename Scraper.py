import os
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scraper(hotelname):
    #store data 
    #edited to read csv from repo
    path_to_file = "Fullerton.csv"
    #number of page to scrape
    num_page = 50

    #url = "https://www.tripadvisor.com.sg/Hotel_Review-g294265-d301679-Reviews-Grand_Copthorne_Waterfront-Singapore.html"
    url = hotelname
    #only for keying in cmd then use
    # if (len(sys.argv) == 4):
    #     path_to_file = sys.argv[1]
    #     num_page = int(sys.argv[2])
    #     url = sys.argv[3]

    #my own environmental path that has seleniumdriver
    #os.environ['PATH'] += r"../SeleniumDrivers"

    #import webdriver my method
    driver = webdriver.Chrome()
    driver.get(url)

    #open file to save review
    csvFile = open(path_to_file, 'w', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    #headings 
    csvWriter.writerow(['TITLE', 'DATE', 'RATING', 'REVIEW'])
    for i in range(0, num_page):

        time.sleep(2)
        #to click Read More
        driver.find_element(By.XPATH, "//span[@class='Ignyf _S Z']").click()

        container = driver.find_elements(By.XPATH, ".//div[@class='YibKl MC R2 Gi z Z BB pBbQr']")

        for j in range(len(container)):
            #title works now
            title = container[j].find_element(By.XPATH,".//a[@class='Qwuub']").text
            date = container[j].find_element(By.XPATH,".//span[@class='teHYY _R Me S4 H3']").text
            rating = container[j].find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
            review = container[j].find_element(By.XPATH,".//q[@class='QewHA H4 _a']").text.replace("\n", " ")

            #df = pd.DataFrame({'Title':title,'Date':date,'Rating':rating, 'Review':review}) 
            #df.to_csv('testingnew.csv', index=False, encoding='utf-8')
            csvWriter.writerow([title ,date ,rating, review])
        
        #to click "Next Page"
        driver.find_element(By.XPATH,".//a[@class='ui_button nav next primary ']").click()

    driver.close()