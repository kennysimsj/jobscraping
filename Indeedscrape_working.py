import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#Extract

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    url = f'https://malaysia.indeed.com/jobs?q=Data%20Scientist&l=Kuala%20Lumpur&start={page}&vjk=db867167e08eafd5'                       # Update this url based on the keyword 
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

#Transform

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('h2').text.strip('new')      #Note: .strip() will remove empty space, and .strip('new') removes the 'new' tag as h2 has two element (the label 'new' and 'jobtitle')
        company = item.find('span', class_ ='companyName').text
        try:                        #because not all jobs have salary)
            salary = item.find('div', class_ ='salary-snippet').text
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n','').replace('â€™','')   
     
    
        #Create Dictionary to store all information
        job =  {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return
   
joblist =[] 

#Decide how many pages to scrape
for i in range(0,40,10):      # range 0 - 40, is going to give from page 1 to 3 in the step of 10, based on webpage structure
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)
    time.sleep(2)           #Time delay to not raise suspicion set to 2s

#Put in dataframe
df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('indeedjobs.csv')



