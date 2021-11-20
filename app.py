#!/nfs/stak/users/croysdaa/.venv3/bin/python
from flask import Flask
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
import pandas as pd
app = Flask(__name__)


@app.route('/')
def index():
    return 'search a job with /search/:keyword/:zipcode/:radius', 200


@app.route('/search/<keyword>/<zipcode>/<radius>', methods=['GET'])
def search(keyword = None, zipcode = None, radius = None):
    #allows program to scrape websites through chrome browser
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    jobs = []


    print('test1')
    #searches a specific job title (keyword, e.g. sales) on linkedin
    driver.get('https://www.linkedin.com/jobs/search/?distance=' + radius + '&geoId=100530215&keywords=' + keyword + '&location=' + zipcode)
    print('test2')
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # this if statement is to make sure that the body is actually included
    if len(list(soup.children)) >= 2:
        html = list(soup.children)[1]
        body = list(html)[2]
        titles = []

        #prints full html page
        #print(list(body))
        
        #print(driver.find_elements_by_class_name('base-search-card_title'))

        # this will be a list of objects that are the jobs from this site
        linkedin_jobs = []

        ### ADD THE JOB TITLES TO THE linkedin_jobs LIST OF OBJECTS
        # enumerate gives a tuple with index and the value at that index
        # in this case, the values in the list are elements, specifically h3
        for index, element in enumerate(soup.findAll('h3', href=False, attrs={'class':'base-search-card__title'})):
            # lstrip removes whitespace at the beginning of a string
            # rstrip removes whitespace at the end of a string
            title = ''.join(element.findAll(text=True)).replace('\n', '').rstrip().lstrip()

            linkedin_jobs.append({ 
                'company': '',
                'title': title,
                'link': '',
                'location': ''
                })

        # TODO make this get the element containing the location
        for index, element in enumerate(soup.findAll('span', href=False, attrs={'class':'job-search-card__location'})):
            location = ''.join(element.findAll(text=True)).replace('\n', '').rstrip().lstrip()
            linkedin_jobs[index]['location'] = location

        # TODO make this get the element containing the company name
        for index, element in enumerate(soup.findAll('a', href=True, attrs={'class':'hidden-nested-link'})):
            company = ''.join(element.findAll(text=True)).replace('\n', '').rstrip().lstrip()
            linkedin_jobs[index]['company'] = company
            print('test3')

        # TODO make this get the element containing the link
        for index, link in enumerate(soup.findAll('a', href=True, attrs={'class':'base-card__full-link'})):
            #link = ''.join(link.findAll())
            linkedin_jobs[index]['link'] = link.get('href')
            print('test4')

        # add the jobs from this site to the master list of jobs
        for job in linkedin_jobs:
            jobs.append(job)

    ##### End of LinkedIn search #####


    #Indeed search
    #driver.get('https://www.indeed.com/jobs?q=' + keyword + '&l=' + zipcode + '&radius=' + radius)

    #content = driver.page_source
    #soup = BeautifulSoup(content, 'lxml')
    #html = list(soup.children)[1]
    #jobs = []

    #print (list(html)[2])

    
    # print(find_elements_by_xpath('//a[@class="job-card-list__title"]'))



    # Quitting selenium driver
    driver.quit()


    # defining JSON to return
    # payload = {
    #         'jobs': jobs
    #         }

    return {'jobs': jobs}, 200

    #response = requests.get('https://www.snagajob.com/')
    #print(response)
    #return response, 200

    # greenhouse_response = requests.get(f'https://boards-api.greenhouse.io/v1/boards/liveperson/jobs')
    # data = greenhouse_response.json()
    # return data, 200

