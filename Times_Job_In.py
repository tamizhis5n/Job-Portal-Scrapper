import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


def times_jobs(job_title,location):
  try:
    job_title_tj = job_title.replace(' ', '+')
    location_tj = location.replace(' ', '+')
    tj_url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=" + str(job_title_tj).replace(' ', '+') + "&txtLocation=" + str(location_tj)
    r = requests.get(tj_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('ul', attrs={'class':'new-joblist'})  
    count=0       
    extracted_data=[]      
    all_titles=[]  
    all_links=[]    
    all_company=[]  
    job_description = []
    for i in results:            
            a=i.find_all('a')                                                                                           
            companies=i.find_all('h3',attrs={'class':'joblist-comp-name'})    
            for j in companies:
                    
                    company=str(j.text).lstrip()
                    company=company.rstrip()
                    all_company.append(company)            
            count=0
            for j in a:
                    if(count%3==0):                                
                            job_title=str(j.text).lstrip()
                            all_titles.append(job_title) 
                            link= str(j['href']).replace(" ", "%20")
                            all_links.append(link)
                            
                    count+=1                 
    for i in range(0,len(all_titles)):                                                    
            extracted_data.append([all_titles[i],
                                  all_company[i],
                                  all_links[i]])
    tj_df = pd.DataFrame(columns=['Job Title', 'Company', 'Link',], data=extracted_data)
    for k in tj_df['Link'].values:
        jd = BeautifulSoup(urllib.request.urlopen(str(k)).read(), 'html.parser')
        jd_res = str(jd.find_all('div', attrs={'class':'jd-sec'})).replace("]", "")
        job_description.append(str(jd_res).replace("[", ""))
    tj_df['Company'] = tj_df['Company'].apply(lambda x: x.replace('(More Jobs)', ''))
    tj_df['Job_Description'] = job_description
    tj_df['Location'] = location
    tj_df['Job_Rec'] = job_title
    return(tj_df)
  except:
    pass