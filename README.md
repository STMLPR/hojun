# 운동 칼로리 소모량 예측 웹 서비스 v2

운동 시간, 체온, 심박수 등의 데이터를 기반으로 운동 중 소모된 칼로리를 예측하는 웹 서비스입니다.
스태킹 앙상블 모델을 사용하여 더 정확한 예측을 제공합니다.

## 시작하기

### 필수 요구사항

- Python 3.9
- pip (Python 패키지 관리자)

### 설치 방법

1. 레포지토리 클론
2. 가상환경 생성 및 활성화
3. 필요한 패키지 설치
    pip install -r requirements.txt


## 실행 방법


1. 웹 서비스 실행
    python app.py
    - 실행 후 http://localhost:5000 접속

## 입력 데이터 범위
| 입력 항목 | 단위 | 허용 범위 |
|---------|------|----------|
| 운동 시간 | 분 | 1~120 |
| 체온 | °C | 35~42 |
| 심박수 | BPM | 60~200 |
| 신장 | cm | 140~200 |
| 체중 | kg | 40~120 |
| 나이 | 세 | 15~80 |
| 성별 | - | 남성/여성 |

## 프로젝트 구조
```
calories-prediction/
├── app_final.py          # Flask 웹 서버 (스태킹 모델)
├── finalModel.ipynb      # 모델 학습 노트북
├── final_model.pkl       # 학습된 스태킹 모델
├── templates/           
│   └── index_final.html  # 메인 페이지
├── static/
│   ├── css/
│   │   └── style_final.css
│   └── js/
│       └── script_final.js
└── README.md
```



## 사용된 모델

스태킹 앙상블 모델에 사용된 기본 모델들:
1. Linear Regression
2. Ridge Regression
3. Random Forest (n_estimators=50)
4. XGBoost (n_estimators=100)
5. LightGBM (n_estimators=100)
6. SVR (kernel='rbf')
7. Elastic Net (alpha=1.0, l1_ratio=0.5)
8. Neural Network (MLP)
9. KNN (n_neighbors=5)

## 전처리 과정

1. 단위 변환
   - 체온: °C → °F
   - 체중: kg → lb
   - 신장: cm → feet & inches

2. 특성 생성
   - PolynomialFeatures(degree=3)로 고차항 생성
   - SelectKBest로 상위 40개 특성 선택

## 기술 스택

- **Backend**
  - Flask 2.0.1
  - Python 3.9

- **Frontend**
  - HTML5/CSS3
  - JavaScript (Vanilla JS)

- **Machine Learning**
  - scikit-learn 1.5.2
  - XGBoost 1.5.0
  - LightGBM 3.3.2
  - pandas 1.3.3
  - numpy 1.23.0

## 팀원

- 이름: 임나경, 이호준, 조세은

## 업데이트 내역

- v2.0.0 (2024-03-21)
  - 스태킹 모델 적용
  - 전처리 과정 개선
  - UI/UX 개선