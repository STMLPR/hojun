from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import pickle

app = Flask(__name__)

# 학습된 모델과 전처리기 로드
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
with open('preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 입력 데이터 받기 (SI 단위로 직접 입력 받음)
        data = {
            'Exercise_Duration': float(request.form['exercise_duration']),
            'Temperature_C': float(request.form['body_temp']),  # 섭씨로 직접 입력
            'BPM': float(request.form['bpm']),
            'Height_cm': float(request.form['height']),  # cm로 직접 입력
            'Weight_kg': float(request.form['weight']),  # kg으로 직접 입력
            'Weight_Status': request.form['weight_status'],
            'Gender': request.form['gender'],
            'Age': int(request.form['age'])
        }
        
        # BMI 계산
        height_m = data['Height_cm'] / 100
        data['BMI'] = data['Weight_kg'] / (height_m ** 2)
        
        # DataFrame으로 변환
        df = pd.DataFrame([data])
        
        # 데이터 전처리
        X_processed = preprocessor.transform(df)
        
        # 예측
        prediction = model.predict(X_processed)[0]
        
        # BMI 상태 판정
        bmi = data['BMI']
        if bmi < 18.5:
            bmi_status = '저체중'
        elif bmi < 23:
            bmi_status = '정상'
        elif bmi < 25:
            bmi_status = '과체중'
        else:
            bmi_status = '비만'
            
        return jsonify({
            'calories': round(prediction, 2),
            'bmi': round(bmi, 1),
            'bmi_status': bmi_status
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 