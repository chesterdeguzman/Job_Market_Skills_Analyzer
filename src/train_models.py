from __future__ import annotations
import argparse, json
from pathlib import Path
import joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression, Ridge


def train(path, model_dir, report_dir):
    df=pd.read_csv(path); train,test=train_test_split(df,test_size=.2,random_state=42,stratify=df['role_category'])
    role_model=Pipeline([('tfidf',TfidfVectorizer(max_features=5000,ngram_range=(1,2))),('model',LogisticRegression(max_iter=1000))])
    role_model.fit(train.job_description,train.role_category); pred=role_model.predict(test.job_description); cls=classification_report(test.role_category,pred,output_dict=True)
    features=['job_title','seniority_level','location','work_mode','industry','skills']; prep=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),features)])
    sal=Pipeline([('prep',prep),('model',Ridge(alpha=10))]); sal.fit(train[features],train.salary_mid_usd); sp=sal.predict(test[features])
    metrics={'role_classifier_accuracy':cls['accuracy'],'role_classifier_macro_f1':cls['macro avg']['f1-score'],'salary_mae_usd':mean_absolute_error(test.salary_mid_usd,sp),'salary_r2':r2_score(test.salary_mid_usd,sp)}
    Path(model_dir).mkdir(parents=True,exist_ok=True); Path(report_dir).mkdir(parents=True,exist_ok=True)
    joblib.dump(role_model,Path(model_dir)/'role_classifier.joblib'); joblib.dump(sal,Path(model_dir)/'salary_model.joblib'); Path(report_dir,'model_metrics.json').write_text(json.dumps(metrics,indent=2)); print(json.dumps(metrics,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--input',default='data/raw/job_postings_synthetic.csv'); p.add_argument('--models',default='models'); p.add_argument('--reports',default='reports'); a=p.parse_args(); train(a.input,a.models,a.reports)
