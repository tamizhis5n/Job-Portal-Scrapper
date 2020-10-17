import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import requests

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def freshersWorld(job_title,location):
    
  try:
    
    X = job_title.replace(" ",'-')
    Y = location.replace(" ",'-')
    url_fw = 'https://www.freshersworld.com/jobs/jobsearch/' + str(X) + '-jobs-in-' + str(Y)
    r_fw = requests.get(url_fw)
    
    soup = BeautifulSoup(r_fw.text, 'html.parser')
    results = soup.find_all('div', attrs={'class':'col-md-12 col-lg-12 col-xs-12', 'style':"margin-bottom: 2%;"})
    jobPost = []
    company = []
    links = []
    job_desc = []
    
    for i in results:      
        var = i.find_all('h3', attrs={'class':'latest-jobs-title font-16 margin-none inline-block'})

        for j in var:
            retrieve = j.text
            company.append(retrieve)

        var = i.find_all('span', attrs={'class':'desc'})
        var=i.find('a')
        links.append(var['href'])
        print(str(var['href']))
        jd = BeautifulSoup(urllib.request.urlopen(str(var['href'])).read(), 'html.parser')
        jd_res = str(jd.find_all('div', attrs={'class':'col-md-12 col-lg-12 col-xs-12 padding-none margin-top-7'})).replace("]", "")
        job_desc.append(striphtml(str(jd_res).replace("[", "")))
        
        var=i.find('div',attrs={'class':'col-md-12 col-xs-12 col-lg-12 padding-none left_move_up' ,'style': 'margin-top: -17px;'})
        retrieve=var.find('div')
        jobPost.append(retrieve.text)

    fw_df = pd.DataFrame({'Job Title':jobPost, 'Company':company, 'Link':links, 'Job_Description':job_desc})
    fw_df['Location'] = location
    fw_df['Job_Rec'] = job_title
    
    return(fw_df)
    
  except:
    pass


if __name__=="__main__":
  #freshersWorld("data scientist","chennai")
  df=freshersWorld(input("Job title?:\n").lower(),input("Job Location?\n").lower())
  df.to_csv("freshersWorld.csv",index=False)