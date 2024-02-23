from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from datetime import date
import xlsxwriter

#Set up Selenium    
options = Options()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(r"C:\Users\megaz\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=options)
driver.get("https://steamcommunity.com/app/1522820/reviews/?browsefilter=mostrecent&snr=1_5_100010_&filterLanguage=schinese&p=1")
wait = WebDriverWait(driver,60);


class Review:
    def __init__(self, rating, date, playtime, content):
        self.rating = rating
        self.date = date
        self.playtime = playtime
        self.content = content

def scrollInfinitePage(reviewsToLoad):
    num_reviews = 0
    while(num_reviews < reviewsToLoad):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # Wait for the number of reviews to increase by 10
        try:
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div.apphub_UserReviewCardContent')) > num_reviews)
            num_reviews += 10
        except TimeoutException:
            print("Timed out waiting for page to load")
            break  # Exit the loop if the page doesn't load

def FindReviewElements():
    reviewBoxDivs = driver.find_elements(By.CSS_SELECTOR, 'div.apphub_UserReviewCardContent')
    return reviewBoxDivs

def extractReviewContent(listOfReviewElements):
    #create a list of reviews
    reviews = []
    for reviewElement in listOfReviewElements:
        ###########Get playtime###########
        playtime = reviewElement.find_element(By.CSS_SELECTOR, 'div.hours').text
        playtime = playtime.split(' ')[0]
        ###########Get rating###########
        rating = reviewElement.find_element(By.CSS_SELECTOR, 'div.thumb').find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        if('thumbsUp' in rating):
            rating = 'Positive'
        else:
            rating = 'Negative'

        ###########Get date###########
        datePostedString = reviewElement.find_element(By.CSS_SELECTOR, 'div.date_posted').text
        #Remove 'Posted: ' from the string
        datePostedString = datePostedString.split('Posted: ')[1]
        #Get day 
        day = datePostedString.split(' ')[0]
        #Get month
        month = datePostedString.split(' ')[1]
        #assign a year (if the review was posted in the current year, it won't be included in the date string)
        year = date.today().year
        #if the date string includes a year, assign it to the year variable
        if len(datePostedString.split(' ')) > 2:
            year = datePostedString.split(' ')[2]
        #occasionally, the day and month are switched in the date string, ensure that the day is always first
        if not day.isdigit():
            tempDay = month
            month = day
            day = tempDay
        #if the year is included in the date string, then a comma will be present after the day, remove it.
        if(',' in day):
            day = day.replace(',', '')
        
        datePosted = day + ' ' + month + ' ' + str(year)

        ###########Get content###########
        if len(reviewElement.find_element(By.CSS_SELECTOR, 'div.apphub_CardTextContent').text.split('\n')) > 1:
            reviewContent = reviewElement.find_element(By.CSS_SELECTOR, 'div.apphub_CardTextContent').text.split('\n')[1]
        #create a new review object and add it to the list of reviews
        newReview = Review(rating, datePosted, playtime, reviewContent)
        reviews.append(newReview)
    return reviews

def outputReviewsToExcel(listOfReviews):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('new.xlsx')
    worksheet = workbook.add_worksheet()

    #Create a header row.    
    row = 0
    col = 0
    header_data = ['Rating', 'Playtime', 'Date', 'Content']
    header_format = workbook.add_format({'bold': True,
                                     'bottom': 2,
                                     'bg_color': '#F9DA04'})
    for item in header_data:
        worksheet.write(row, col, item, header_format)
        col += 1
    
    #Insert the data into the worksheet.
    col = 0
    row = 1
    for review in listOfReviews:
        worksheet.write(row, col, review.rating)
        worksheet.write(row, col + 1, review.playtime)
        worksheet.write(row, col + 2, review.date)
        worksheet.write(row, col + 3, review.content)
        row += 1    
    worksheet.autofit()

    #Close the workbook.
    workbook.close()

def main():
    scrollInfinitePage(7000)
    reviewElements = FindReviewElements()
    reviews = extractReviewContent(reviewElements)
    outputReviewsToExcel(reviews)

    driver.quit()


main()