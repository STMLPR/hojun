from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression
import pickle

app = Flask(__name__)

# 모델과 전처리기 로드
try:
    with open('final_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        stacking = model_data['model']
        poly = model_data['poly']
        selector = model_data['selector']
    print("모델 로드 성공")
except Exception as e:
    print(f"모델 로드 실패: {str(e)}")
    # 기본값 설정
    poly = PolynomialFeatures(degree=3, include_bias=False)
    selector = SelectKBest(score_func=f_regression, k=40)

def create_features(data):
    """기본 특성 생성 - 학습 시와 동일한 특성만 사용"""
    # train_x에 남은 특성들: Exercise_Duration, Body_Temperature(F), BPM, Weight(lb), Gender, Age
    features = pd.DataFrame([{
        'Exercise_Duration': float(data['exercise_duration']),
        'Body_Temperature(F)': (float(data['body_temp']) * 9/5) + 32,
        'BPM': float(data['bpm']),
        'Weight(lb)': float(data['weight']) * 2.20462,
        'Gender': 1 if data['gender'] == 'M' else 0,
        'Age': float(data['age'])
    }])
    
    # 학습 시와 동일한 컬럼 순서로 정렬
    expected_columns = [
        'Exercise_Duration', 'Body_Temperature(F)', 'BPM', 
        'Weight(lb)', 'Gender', 'Age'
    ]
    features = features[expected_columns]
    
    return features

def preprocess_input(data):
    """입력 데이터 전처리"""
    try:
        # 기본 특성 생성
        features = create_features(data)
        print("Features shape:", features.shape)
        print("Features columns:", features.columns.tolist())
        
        # 다항식 특성 생성
        poly_features = poly.transform(features)
        print("Poly features shape:", poly_features.shape)
        
        # 특성 선택 적용
        selected_features = selector.transform(poly_features)
        print("Selected features shape:", selected_features.shape)
        
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
        # 입력 데이터 ��기
        data = {
            'exercise_duration': request.form['exercise_duration'],
            'body_temp': request.form['body_temp'],
            'bpm': request.form['bpm'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'gender': request.form['gender'],
            'age': request.form['age']
        }
        
        # 데이터 전처리
        processed_data = preprocess_input(data)
        
        # 예측
        prediction = stacking.predict(processed_data)[0]
        
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