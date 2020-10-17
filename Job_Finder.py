from Indeed_in import indeed
from FreshersWorld_IN import freshersWorld
from Times_Job_In import times_jobs
import pandas as pd
def main(job,loc):
    a=indeed(job,loc)
    b=freshersWorld(job,loc)
    c=times_jobs(job,loc)
    d=pd.concat([a,b,c])
    d.to_csv("Jobs_list.csv",index=False)

if __name__=="__main__":
  #freshersWorld("data scientist","chennai")
  main(input("Job title?:\n").lower(),input("Job Location?\n").lower())
