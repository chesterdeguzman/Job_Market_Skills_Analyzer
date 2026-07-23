from src.generate_dataset import generate

def test_generator_schema():
    df=generate(100,1)
    assert len(df)==100
    assert {'role_category','salary_mid_usd','skills','work_mode'}.issubset(df.columns)
    assert df['salary_mid_usd'].gt(0).all()
