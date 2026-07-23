# Job Market Skills Analyzer

An end-to-end Python portfolio project that analyzes job postings to identify demanded skills, salary patterns, remote-work trends, and differences among Data Analyst, Data Scientist, Data Engineer, and BI Analyst roles.

> **Data note:** The included dataset is synthetic and generated specifically for portfolio practice. It does not represent live job postings or verified market statistics.

## What the project delivers
- Top Python, SQL, BI, cloud, and machine-learning skills
- Salary comparisons by skill, role, seniority, and location
- Remote, hybrid, and on-site trends by quarter
- Analyst-versus-scientist role comparison
- NLP job-role classifier
- Salary prediction baseline
- Interactive Streamlit dashboard
- Reproducible synthetic-data generator
- Automated tests and GitHub Actions

## Dataset
`data/raw/job_postings_synthetic.csv` contains 25,000 synthetic postings covering January 2024 through June 2026.

Main columns include job title, role category, seniority, company, industry, location, work mode, salary, experience, skills, and job description.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/analyze.py
python src/train_models.py
streamlit run dashboard/app.py
```

Regenerate the dataset:
```bash
python src/generate_dataset.py --rows 25000 --seed 42
```

## Repository structure
```text
data/raw/              included synthetic dataset
data/processed/        optional processed outputs
src/                    generator, analysis, and modeling code
reports/figures/        charts
reports/tables/         analysis tables
models/                 trained models
notebooks/              notebook workspace
dashboard/app.py        Streamlit application
tests/                  automated tests
```

## Responsible use
This repository is for education and portfolio demonstration. Do not present the synthetic results as current labor-market facts. For production use, replace the dataset with legally obtained postings and document collection dates, geography, coverage, and sampling limitations.
