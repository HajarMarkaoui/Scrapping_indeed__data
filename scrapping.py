#import libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd

##########################################################User parameters######################################################
                                              ################# Enter parameters here #######################

position='Actuaire'
location='Paris'

######### Subsidaries functions #########
def construct_url(position,location):
    """ generate url from position and location """
    
    template='https://fr.indeed.com/jobs?q={position}&l={location}' 
    url=template.format(position=position,location=location)
    return url


def get_url(url):
    ''' generate the http request function '''
    
    r=requests.get(url)
    html_data=r.text
    return html_data

    
def get_html(html_data):
    '''  Parse the html with Beautiful soup '''
    
    soup=BeautifulSoup(html_data,'html.parser')
    return soup

def get_record(card):
    ''' Function to get one record from a specific card '''
    job_title=card.find(class_='jobTitle').get_text()
    company_location=card.find('div','companyLocation').get_text()
    company_name=card.find('span','companyName').get_text()
    summary=card.find(class_='job-snippet').get_text()
    today=datetime.today().strftime("%d/%m/%Y")
    
    try:
        job_salary=card.find(class_='salary-snippet').get_text()
    except AttributeError:
        job_salary=''
    record=(job_title,company_location,company_name,summary,job_salary,today)
    return record

def save_positions(path,df):
    df.to_csv(path,encoding='utf-8-sig',sep=';')
    
    
    
############################################### Main function ###############################################################

def scrape(position,location):
      
    ''' the main function for scrapping '''
    records=[]
    
   
    
    url=construct_url(position, location)
    html_data=get_url(url)
    soup=get_html(html_data)
    
    
    url=construct_url(position, location)
    html_data=get_url(url)
    soup=get_html(html_data)
    
    #get the number of pages
    
    pagination = soup.find("ul","pagination-list").find_all('li')
    pages=len(pagination)

  
    #Extraction for the first page
    
    cards=soup.find_all('div','job_seen_beacon') 
    print(cards)
    for card in cards:
        records.append(get_record(card))
        
        
    #Extraction for the folowing pages 
    
    for x in range(1,pages):
        page_append = "&start=" + str(x*10)
        current_page ='https://fr.indeed.com/jobs?q=actuaire&l=Paris%20(75)'+page_append
        html_data=get_url(current_page)
        soup=get_html(html_data)
        cards=soup.find_all('div','job_seen_beacon')
        for card in cards:
            records.append(get_record(card))
            
    #Creation of a dataFrame with all records
    
    df=pd.DataFrame(records,columns=['Job Title','Company location','Company Name','Summary','Job Salary','Extraction Date'])
    print(df['company name'])
    save_positions('C:\work\scrapping\positions.csv',df)
                
results=print(scrape(position,location))