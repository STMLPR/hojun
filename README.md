# 운동 칼로리 소모량 예측 웹 서비스

운동 시간, 체온, 심박수 등의 데이터를 기반으로 운동 중 소모된 칼로리를 예측하는 웹 서비스입니다.

## 시작하기

### 필수 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. 레포지토리 클론
2. 가상환경 생성 및 활성화
3. 필요한 패키지 설치
    pip install -r requirements.txt


## 실행 방법

### 1. 모델 학습
    python train_model.py
- 실행 후 생성되는 파일들:
  - `model.pkl`: 학습된 LightGBM 모델
  - `preprocessor.pkl`: 데이터 전처리기
  - `submission.csv`: 테스트 데이터 예측 결과

### 2. 웹 서비스 실행
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
| 체중상태 | - | 정상/과체중 |

## 프로젝트 구조
exercise-calories-prediction/
├── app.py # Flask 웹 서버
├── train_model.py # 모델 학습 스크립트
├── templates/ # HTML 템플릿
│ └── index.html # 메인 페이지
├── model.pkl # 학습된 모델 (생성됨)
├── preprocessor.pkl # 전처리기 (생성됨)
├── requirements.txt # 필요한 패키지 목록
└── README.md # 프로젝트 설명


## 주요 파일 설명

### 1. train_model.py
- 데이터 전처리 및 변환 (단위 변환: 영국식 → 미터법)
- LightGBM 모델 학습 (최적 하이퍼파라미터 적용)
- 모델 및 전처리기 저장

### 2. app.py
- Flask 웹 서버 구현
- 모델 및 전처리기 로드
- BMI 계산 및 체중상태 판정
- 예측 API 엔드포인트 제공

### 3. index.html
- 반응형 웹 디자인 (Bootstrap 5)
- 실시간 입력값 검증
- AJAX를 통한 비동기 예측 요청
- 예측 결과 및 BMI 정보 표시

## 기술 스택

- **Backend**
  - Flask 2.0.1
  - Python 3.8+

- **Frontend**
  - HTML5/CSS3
  - JavaScript (jQuery)
  - Bootstrap 5.1.3

- **Machine Learning**
  - LightGBM 3.3.2
  - scikit-learn 0.24.2
  - pandas 1.3.3
  - numpy 1.21.2

## 문제 해결

### 자주 발생하는 오류

1. ModuleNotFoundError
   - 해결: `pip install -r requirements.txt` 실행

2. 모델 파일 없음 오류
   - 해결: `python train_model.py` 실행하여 모델 생성

3. 포트 충돌
   - 해결: app.py에서 다른 포트 번호 지정
   ```python
   app.run(port=다른_포트번호)
   ```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 작성자

- 이름: 이호준
- GitHub: https://github.com/Nutcracker5286

## 업데이트 내역

- v1.0.0 (2024-03-21)
  - 최초 릴리즈
  - SI 단위계 적용
  - 웹 인터페이스 구현