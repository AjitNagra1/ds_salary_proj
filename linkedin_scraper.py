# import libraries (selenium and time)
import time
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# keep window open
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# define path for the driver
PATH = "C:\Program Files (x86)\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH,chrome_options=chrome_options)

# launch the browser to full screen
driver.maximize_window() 
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# enter the site
driver.get("https://www.linkedin.com/jobs/")
# make the program wait 2s to ensure page is loaded
time.sleep(2)

# accept cookies and click 'accept'
cookies = driver.find_element(By.XPATH,"""//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]""").click()

# User Credentials
# Reading txt file where we have our user credentials
with open('user_credentials.txt', 'r',encoding="utf-8") as file:
    user_credentials = file.readlines()
    user_credentials = [line.rstrip() for line in user_credentials]
user_name = user_credentials[0] # First line
pass_word = user_credentials[1] # Second line
username = driver.find_element(By.XPATH,"""//*[@id="session_key"]""").send_keys(user_name)
password = driver.find_element(By.XPATH,"""//*[@id="session_password"]""").send_keys(pass_word)
time.sleep(1)

# find and click login
login=driver.find_element(By.XPATH,"""//*[@id="main-content"]/section[1]/div/div/form/button""").click()

# on homescreen click jobs
jobs=driver.find_element(By.XPATH,"""//*[@id="global-nav"]/div/nav/ul/li[3]/a""").click()
time.sleep(3)

# Go to search results directly via link
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3436497337&f_E=2%2C3%2C4&f_JT=F%2CC&f_WT=2%2C3&geoId=101165590&keywords=energy%20analyst&location=United%20Kingdom&refresh=true")
time.sleep(1)

# access the job list on the left hand side of the page
# job_block = driver.find_element(By.CLASS_NAME,"job-search-results-list")
# job_list = driver.find_elements(By.CLASS_NAME,"scaffold-layout__list-container")

jobs_block = driver.find_element(By.CLASS_NAME,"jobs-search-results-list")
jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, "jobs-search-results__list-item")

# Using loop to check every job card in the job list

# Get all links for these offers
links = []
# Navigate 13 pages
print('Links are being collected now.')
try: 
    for page in range(2,6):
        time.sleep(1)
        jobs_block = driver.find_element(By.CLASS_NAME,'jobs-search-results-list')
        jobs_list= jobs_block.find_elements(By.CSS_SELECTOR,'.jobs-search-results__list-item')
    
        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME,'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        
        print(f'Collecting the links in the page: {page-1}')
        # go to next page:
        driver.find_element(By.XPATH,f"//button[@aria-label='Page {page}']").click()
        time.sleep(2)
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers')

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []

i = 0
j = 1

# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(1)
        # Click See more.
        driver.find_element(By.CLASS_NAME,"artdeco-card__actions").click()
        time.sleep(1)
    except:
        pass
 
    # Find the general information of the job offers
    contents = driver.find_elements(By.CLASS_NAME,'p5')
    for content in contents:
        try:
            job_titles.append(content.find_element(By.TAG_NAME,"h1").text)
            company_names.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__job-insight").text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+= 1
        except:
            pass
        time.sleep(1)
        
        # Scraping the job description
    job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(1)  
            
# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
                    company_locations,work_methods,
                    post_dates,work_times)),
                    columns =['job_title', 'company_name',
                           'company_location','work_method',
                           'post_date','work_time'])

# Storing the data to csv file
df.to_csv('job_offers.csv', index=False)

# Output job descriptions to txt file
with open('job_descriptions.txt', 'w',encoding="utf-8") as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')