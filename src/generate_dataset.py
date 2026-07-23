from __future__ import annotations
import argparse, random
from pathlib import Path
import numpy as np
import pandas as pd

ROLES = {
    'Data Analyst': ['SQL','Excel','Power BI','Tableau','Python','Pandas','Data Visualization','Statistics'],
    'Data Scientist': ['Python','SQL','Scikit-learn','Machine Learning','Pandas','NumPy','Statistics','TensorFlow','PyTorch'],
    'Data Engineer': ['SQL','Python','Spark','AWS','Azure','Databricks','Snowflake','Airflow','Docker'],
    'BI Analyst': ['Power BI','SQL','Excel','Tableau','DAX','Data Visualization','ETL'],
}
BASE_SALARY = {'Data Analyst':70000,'Data Scientist':105000,'Data Engineer':110000,'BI Analyst':76000}
LEVEL_MULT = {'Entry':0.82,'Mid':1.00,'Senior':1.28,'Lead':1.50}
LOCATIONS = {
    'New York, NY':1.18,'San Francisco, CA':1.30,'Seattle, WA':1.18,'Austin, TX':1.02,
    'Chicago, IL':1.00,'Boston, MA':1.12,'Atlanta, GA':0.94,'Denver, CO':1.00,
    'Dallas, TX':0.96,'Remote - US':1.05
}
COMPANIES = ['Northstar Analytics','BluePeak Health','Orbit Commerce','Vertex Financial','Nova Retail','Cloudline Systems','Summit Media','Greenfield Energy','Apex Logistics','BrightPath Consulting']
INDUSTRIES = ['Technology','Finance','Healthcare','Retail','Consulting','Media','Energy','Logistics']
SKILL_PREMIUM = {'Spark':9000,'Snowflake':7000,'Databricks':8500,'AWS':6000,'Azure':5500,'TensorFlow':6500,'PyTorch':6500,'Machine Learning':8000,'Power BI':2500,'Tableau':2200,'SQL':1800,'Python':3000}


def make_description(role, level, skills, work_mode):
    return (f"We are hiring a {level.lower()} {role} to support business decision-making. "
            f"The successful candidate will work in a {work_mode.lower()} environment and use "
            f"{', '.join(skills[:6])}. Responsibilities include data cleaning, analysis, reporting, "
            "stakeholder communication, dashboard development, and translating findings into recommendations.")


def generate(n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed); random.seed(seed)
    rows=[]
    start=pd.Timestamp('2024-01-01'); end=pd.Timestamp('2026-06-30')
    for i in range(n):
        role=random.choices(list(ROLES), weights=[36,25,22,17])[0]
        level=random.choices(list(LEVEL_MULT), weights=[28,42,24,6])[0]
        location=random.choice(list(LOCATIONS))
        if location=='Remote - US': work_mode='Remote'
        else: work_mode=random.choices(['On-site','Hybrid','Remote'], weights=[44,38,18])[0]
        core=ROLES[role]
        k=random.randint(4,min(8,len(core)))
        skills=random.sample(core,k)
        optional=['Git','Docker','GCP','R','Looker','dbt','Jupyter','GitHub','BigQuery','PostgreSQL']
        skills += random.sample(optional, random.randint(0,3))
        skills=list(dict.fromkeys(skills))
        date=start + pd.to_timedelta(int(rng.integers(0,(end-start).days+1)), unit='D')
        remote_trend=(date.year-2024)*0.04
        if work_mode=='On-site' and rng.random()<remote_trend: work_mode='Hybrid'
        salary=BASE_SALARY[role]*LEVEL_MULT[level]*LOCATIONS[location]
        salary += sum(SKILL_PREMIUM.get(s,0) for s in skills)
        if work_mode=='Remote': salary*=1.03
        salary *= rng.normal(1,0.08)
        midpoint=round(salary,-2); spread=random.choice([8000,10000,12000,15000])
        low=max(35000,midpoint-spread/2); high=midpoint+spread/2
        rows.append({
            'job_id':f'JOB-{i+1:06d}','posting_date':date.date(),'job_title':f'{level} {role}',
            'role_category':role,'seniority_level':level,'company':random.choice(COMPANIES),
            'industry':random.choice(INDUSTRIES),'location':location,'work_mode':work_mode,
            'employment_type':random.choices(['Full-time','Contract','Part-time'],[88,10,2])[0],
            'salary_min_usd':int(low),'salary_max_usd':int(high),'salary_mid_usd':int((low+high)/2),
            'years_experience':{'Entry':random.randint(0,2),'Mid':random.randint(2,5),'Senior':random.randint(5,9),'Lead':random.randint(8,14)}[level],
            'skills':'; '.join(skills),'job_description':make_description(role,level,skills,work_mode),
            'source':'Synthetic portfolio dataset','is_synthetic':True
        })
    return pd.DataFrame(rows)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--rows',type=int,default=25000); p.add_argument('--seed',type=int,default=42); p.add_argument('--output',default='data/raw/job_postings_synthetic.csv')
    a=p.parse_args(); df=generate(a.rows,a.seed); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); df.to_csv(out,index=False); print(f'Wrote {len(df):,} rows to {out}')
