from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def explode_skills(df):
    x=df[['job_id','role_category','salary_mid_usd','skills']].copy()
    x['skill']=x['skills'].str.split('; ')
    return x.explode('skill')


def run(input_path, out_dir):
    out=Path(out_dir); (out/'figures').mkdir(parents=True,exist_ok=True); (out/'tables').mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(input_path,parse_dates=['posting_date']); ex=explode_skills(df)
    top=ex['skill'].value_counts().rename_axis('skill').reset_index(name='postings')
    salary=ex.groupby('skill')['salary_mid_usd'].agg(['count','median','mean']).query('count >= 100').sort_values('median',ascending=False).reset_index()
    remote=df.groupby(['posting_date','work_mode']).size().reset_index(name='jobs'); remote['quarter']=remote['posting_date'].dt.to_period('Q').astype(str)
    remote_q=remote.groupby(['quarter','work_mode'])['jobs'].sum().reset_index()
    role=df.groupby('role_category').agg(postings=('job_id','count'),median_salary=('salary_mid_usd','median'),remote_share=('work_mode',lambda s:(s=='Remote').mean()),hybrid_share=('work_mode',lambda s:(s=='Hybrid').mean()),median_experience=('years_experience','median')).reset_index()
    role_skill=ex.groupby(['role_category','skill']).size().reset_index(name='postings'); role_skill['rank']=role_skill.groupby('role_category')['postings'].rank(method='first',ascending=False); role_skill=role_skill[role_skill['rank']<=10]
    for name,t in [('top_skills.csv',top),('salary_by_skill.csv',salary),('remote_trends.csv',remote_q),('role_comparison.csv',role),('top_skills_by_role.csv',role_skill)]: t.to_csv(out/'tables'/name,index=False)

    ax=top.head(20).sort_values('postings').plot.barh(x='skill',y='postings',legend=False,title='Top 20 Requested Skills'); ax.set_xlabel('Job postings'); plt.tight_layout(); plt.savefig(out/'figures'/'top_skills.png',dpi=160); plt.close()
    pivot=remote_q.pivot(index='quarter',columns='work_mode',values='jobs').fillna(0); share=pivot.div(pivot.sum(axis=1),axis=0); share.plot(title='Work Mode Share by Quarter'); plt.ylabel('Share of postings'); plt.tight_layout(); plt.savefig(out/'figures'/'remote_trends.png',dpi=160); plt.close()
    ax=role.sort_values('median_salary').plot.barh(x='role_category',y='median_salary',legend=False,title='Median Salary by Role'); ax.set_xlabel('USD'); plt.tight_layout(); plt.savefig(out/'figures'/'salary_by_role.png',dpi=160); plt.close()
    summary={'rows':len(df),'date_min':str(df.posting_date.min().date()),'date_max':str(df.posting_date.max().date()),'median_salary':float(df.salary_mid_usd.median()),'remote_share':float((df.work_mode=='Remote').mean()),'top_10_skills':top.head(10).to_dict('records')}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--input',default='data/raw/job_postings_synthetic.csv'); p.add_argument('--out',default='reports'); a=p.parse_args(); run(a.input,a.out)
