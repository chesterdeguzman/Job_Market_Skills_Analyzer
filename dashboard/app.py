import pandas as pd
import streamlit as st
st.set_page_config(page_title='Job Market Skills Analyzer',layout='wide')
@st.cache_data
def load(): return pd.read_csv('data/raw/job_postings_synthetic.csv',parse_dates=['posting_date'])
df=load(); st.title('Job Market Skills Analyzer'); st.caption('Synthetic portfolio dataset — not live labor-market data')
roles=st.sidebar.multiselect('Role',sorted(df.role_category.unique()),default=sorted(df.role_category.unique())); modes=st.sidebar.multiselect('Work mode',sorted(df.work_mode.unique()),default=sorted(df.work_mode.unique())); x=df[df.role_category.isin(roles)&df.work_mode.isin(modes)]
c1,c2,c3=st.columns(3); c1.metric('Postings',f'{len(x):,}'); c2.metric('Median salary',f'${x.salary_mid_usd.median():,.0f}'); c3.metric('Remote share',f'{(x.work_mode=="Remote").mean():.1%}')
sk=x.assign(skill=x.skills.str.split('; ')).explode('skill').skill.value_counts().head(20); st.subheader('Top skills'); st.bar_chart(sk)
st.subheader('Role comparison'); st.dataframe(x.groupby('role_category').agg(postings=('job_id','count'),median_salary=('salary_mid_usd','median'),remote_share=('work_mode',lambda s:(s=='Remote').mean())).reset_index(),use_container_width=True)
st.subheader('Remote-work trend'); q=x.assign(quarter=x.posting_date.dt.to_period('Q').astype(str)).groupby(['quarter','work_mode']).size().unstack(fill_value=0); st.line_chart(q.div(q.sum(axis=1),axis=0))
