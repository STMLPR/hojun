from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression
import pickle
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.svm import SVR
import os
import warnings

warnings.filterwarnings('ignore')  # 경고 메시지 숨기기
app = Flask(__name__)

# 기본 모델 및 전처리기 설정
def create_base_models():
    return [
        ('linear', LinearRegression()),
        ('ridge', Ridge()),
        ('rf', RandomForestRegressor(n_estimators=50, random_state=42)),
        ('xgb', XGBRegressor(n_estimators=100, random_state=42)),
        ('lgbm', LGBMRegressor(n_estimators=100, random_state=42)),
        ('svr', SVR(kernel='rbf')),
        ('elastic', ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42)),
        ('mlp', MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42)),
        ('knn', KNeighborsRegressor(n_neighbors=5))
    ]

# 전역 변수로 모델과 전처리기 선언
stacking = None
poly = None
selector = None

def init_model():
    global stacking, poly, selector
    
    try:
        # 모델 로드 시도
        with open('final_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
            
        if isinstance(model_data, dict):
            stacking = model_data['model']
            poly = model_data['poly']      # 직접 저장된 전처리기 사용
            selector = model_data['selector']  # 직접 저장된 전처리기 사용
            print("기존 모델 로드 성공!")
            return True
            
    except Exception as e:
        print(f"모델 로드 실패 상세: {str(e)}")
        
        # 새로운 모델 생성
        base_models = create_base_models()
        stacking = StackingRegressor(
            estimators=base_models,
            final_estimator=Ridge(alpha=1.0),
            cv=5
        )
        
        # ipynb와 동일한 전처리기 생성
        poly = PolynomialFeatures(degree=3)  # include_bias=True가 기본값
        selector = SelectKBest(score_func=f_regression, k=40)
        
        print("새로운 모델 생성 완료!")
        return False

# 앱 시작 시 모델 초기화
init_model()

def create_features(data):
    """입력 데이터로부터 특성 생성"""
    features = pd.DataFrame([{
        'Exercise_Duration': float(data['exercise_duration']),
        'Body_Temperature(F)': (float(data['body_temp']) * 9/5) + 32,
        'BPM': float(data['bpm']),
        'Weight(lb)': float(data['weight']) * 2.20462,
        'Height(Feet)': float(data['height']) / 30.48,  # cm를 feet로 변환
        'Height(Remainder_Inches)': (float(data['height']) / 2.54) % 12,  # cm를 inch로 변환하고 나머지
        'Gender': 1 if data['gender'] == 'M' else 0,  # Gender는 LabelEncoder 대신 직접 변환
        'Age': float(data['age']),
        'Weight_Status': 'Normal' if float(data['weight']) / ((float(data['height'])/100) ** 2) < 25 else 'Overweight'
    }])
    
    # Weight_Status와 Height 관련 컬럼 제거
    features = features.drop(['Weight_Status', 'Height(Remainder_Inches)', 'Height(Feet)'], axis=1)
    
    # ipynb와 동일한 컬럼 순서로 반환
    return features[['Exercise_Duration', 'Body_Temperature(F)', 'BPM', 
                    'Weight(lb)', 'Gender', 'Age']]

def preprocess_input(data):
    """입력 데이터 전처리"""
    try:
        features = create_features(data)
        poly_features = poly.transform(features)
        selected_features = selector.transform(poly_features)
        return selected_features
        
    except Exception as e:
        print(f"전처리 중 오류 발생: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index_final.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'exercise_duration': request.form['exercise_duration'],
            'body_temp': request.form['body_temp'],
            'bpm': request.form['bpm'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'gender': request.form['gender'],
            'age': request.form['age']
        }
        
        processed_data = preprocess_input(data)
        prediction = stacking.predict(processed_data)[0]
        
        # 음수 값 방지
        prediction = max(0, prediction)
        
        # BMI 계산
        height_m = float(data['height']) / 100
        weight_kg = float(data['weight'])
        bmi = weight_kg / (height_m ** 2)
        
        # BMI 상태 판정
        if bmi < 18.5:
            bmi_status = '저체중'
        elif bmi < 23:
            bmi_status = '정상'
        elif bmi < 25:
            bmi_status = '과체중'
        else:
            bmi_status = '비만'
            
        return jsonify({
            'calories': round(float(prediction), 2),
            'bmi': round(float(bmi), 1),
            'bmi_status': bmi_status
        })
    
    except Exception as e:
        print(f"예측 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)