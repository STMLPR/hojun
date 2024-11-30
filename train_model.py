import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import lightgbm as lgb
import pickle

def preprocess_data(df):
    # 단위 변환
    df['Temperature_C'] = (df['Body_Temperature(F)'] - 32) * 5/9
    df['Height_cm'] = (df['Height(Feet)'] * 30.48) + (df['Height(Remainder_Inches)'] * 2.54)
    df['Weight_kg'] = df['Weight(lb)'] * 0.453592
    df['BMI'] = df['Weight_kg'] / ((df['Height_cm']/100) ** 2)
    
    # 불필요한 컬럼 제거
    columns_to_drop = ['ID', 'Body_Temperature(F)', 'Height(Feet)', 
                      'Height(Remainder_Inches)', 'Weight(lb)']
    return df.drop(columns_to_drop, axis=1)

def create_preprocessor():
    # 수치형 특성과 범주형 특성 구분
    numeric_features = ['Exercise_Duration', 'BPM', 'Age', 
                       'Temperature_C', 'Height_cm', 'Weight_kg', 'BMI']
    categorical_features = ['Weight_Status', 'Gender']
    
    # 전처리 파이프라인 생성
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop='first', sparse=False)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor, numeric_features, categorical_features

def train_model():
    # 데이터 로드
    train = pd.read_csv('train.csv')
    test = pd.read_csv('test.csv')
    
    # 데이터 전처리
    train_processed = preprocess_data(train)
    
    # 특성과 타겟 분리
    X = train_processed.drop('Calories_Burned', axis=1)
    y = train_processed['Calories_Burned']
    
    # 전처리기 생성
    preprocessor, numeric_features, categorical_features = create_preprocessor()
    
    # 데이터 전처리
    X_processed = preprocessor.fit_transform(X)
    
    # 최적 하이퍼파라미터로 모델 학습
    model = lgb.LGBMRegressor(
        objective='regression',
        colsample_bytree=0.8749080237694725,
        learning_rate=0.05753571532049581,
        max_depth=5,
        min_child_samples=27,
        min_child_weight=1e-05,
        n_estimators=288,
        num_leaves=40,
        reg_alpha=0,
        reg_lambda=0,
        subsample=0.8312037280884873,
        random_state=42
    )
    
    # 모델 학습
    print("모델 학습 시작...")
    model.fit(X_processed, y)
    
    # 모델과 전처리기 저장
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('preprocessor.pkl', 'wb') as f:
        pickle.dump(preprocessor, f)
    
    print("모델 학습 및 저장 완료!")
    
    # 테스트 데이터 예측
    test_processed = preprocess_data(test)
    X_test_processed = preprocessor.transform(test_processed)
    test_pred = model.predict(X_test_processed)
    
    # 제출 파일 생성
    submission = pd.DataFrame({
        'ID': test['ID'],
        'Calories_Burned': test_pred
    })
    submission.to_csv('submission.csv', index=False)
    print("예측 완료! submission.csv 파일이 생성되었습니다.")

if __name__ == "__main__":
    train_model()