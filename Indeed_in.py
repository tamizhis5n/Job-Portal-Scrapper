import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

import re
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def indeed(job_title,location):

  
  X = job_title.replace(" ",'-')
  Y = location.replace(" ",'-')
  URL="https://www.indeed.co.in/"+X+"-jobs-in-"+Y
  #print(URL)
  soup = BeautifulSoup(urllib.request.urlopen(URL).read(), 'html.parser')
  #print("32")

  results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
  a=[]
  b=[]
  c = []
  d = []
  #print(results)
  #print("32")
  for x in results:
      company = x.find('span', attrs={"class":"company"})
      if company:
          a.append(company.text.strip())
      job = x.find('a', attrs={'data-tn-element': "jobTitle"})
      if job:
          b.append(job.text.strip())
      link = x.find('a', href=True, attrs={'data-tn-element':'jobTitle'})
      link = str('https://www.indeed.co.in' + link['href'])
      print (link)
      if link:
          c.append(link)
      jd = BeautifulSoup(urllib.request.urlopen(link).read(), 'html.parser')
      jd_res = str(jd.find_all('div', attrs={'id': 'jobDescriptionText', 'class':'jobsearch-jobDescriptionText'})).replace("]", "")
      #jd_res = [x.find('div') for x in jd_res]
      zz=str(jd_res).replace("[", "")
      print(zz)
      print(striphtml(zz))
      d.append(striphtml(zz))
  #print(a)
  #print(b) 
  #print(c)
  #print(d)   
  #print("@@@@@@@@@")    
  indeed_df = pd.DataFrame(list(zip(b, a, c, d)),columns =['Job Title', 'Company', 'Link', 'Job_Description']) 
  indeed_df['Location'] = location
  indeed_df['Job_Rec'] = job_title
  return(indeed_df)


if __name__=="__main__":
  #indeed("data scientist","chennai")
  df=indeed(input("Job title?:\n").lower(),input("Job Location?\n").lower())
  df.to_csv("Indeed.csv",index=False)