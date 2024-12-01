document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');
    const exampleButton = document.querySelector('.example-button');
    
    submitButton.disabled = true;
    submitButton.textContent = '예측 중...';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('에러가 발생했습니다: ' + data.error);
            return;
        }
        
        // 결과 표시
        const result = document.getElementById('result');
        result.style.opacity = '0';
        result.classList.remove('hidden');
        
        document.getElementById('calories').textContent = data.calories;
        document.getElementById('bmi').textContent = data.bmi;
        document.getElementById('bmi-status').textContent = data.bmi_status;
        
        // Fade in 애니메이션
        setTimeout(() => {
            result.style.transition = 'opacity 0.5s ease';
            result.style.opacity = '1';
        }, 100);
        
        // 예시 데이터 버튼 숨기기
        exampleButton.style.display = 'none';
        
        // 부드러운 스크롤
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
    } catch (error) {
        alert('서버 오류가 발생했습니다. 다시 시도해주세요.');
        console.error('Error:', error);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = '예측하기';
    }
});

// 입력값 예시 데이터
const exampleData = {
    exercise_duration: 15,
    body_temp: 36.5,
    bpm: 80,
    height: 170,
    weight: 65,
    age: 30
};

// 예시 데이터 채우기 버튼 추가
const fillExampleButton = document.createElement('button');
fillExampleButton.textContent = '예시 데이터 채우기';
fillExampleButton.className = 'example-button';
fillExampleButton.onclick = (e) => {
    e.preventDefault();
    Object.keys(exampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = exampleData[key];
            validateInput(input);
        }
    });
};

document.querySelector('form').insertBefore(
    fillExampleButton, 
    document.querySelector('button[type="submit"]')
);

// 입력값 검증 함수
function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    // exercise_duration은 상한 체크 제외
    if (input.id === 'exercise_duration') {
        if (value >= min) {
            input.style.borderColor = '#27ae60';
            input.parentElement.querySelector('.range-info').style.color = '#27ae60';
            return true;
        }
    } else {
        // 다른 입력값들은 min, max 모두 체크
        if (value >= min && (max ? value <= max : true)) {
            input.style.borderColor = '#27ae60';
            input.parentElement.querySelector('.range-info').style.color = '#27ae60';
            return true;
        }
    }
    
    input.style.borderColor = '#e74c3c';
    input.parentElement.querySelector('.range-info').style.color = '#e74c3c';
    return false;
}

// 모든 숫자 입력 필드에 대한 이벤트 리스너
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', () => validateInput(input));
    
    // 포커스 아웃 시 소수점 자리 정리
    input.addEventListener('blur', () => {
        const value = parseFloat(input.value);
        if (!isNaN(value)) {
            input.value = value.toFixed(1);
            validateInput(input);
        }
    });
});

// 다시하기 버튼 이벤트 추가
document.getElementById('reset-button').addEventListener('click', () => {
    // 폼 초기화
    document.getElementById('prediction-form').reset();
    
    // 결과 숨기기
    document.getElementById('result').classList.add('hidden');
    
    // 예시 데이터 버튼 다시 표시
    document.querySelector('.example-button').style.display = 'block';
    
    // 모든 입력 필드 초기화
    document.querySelectorAll('input').forEach(input => {
        input.style.borderColor = '#dcdde1';  // CSS 변수 대신 직접 색상 지정
        const rangeInfo = input.parentElement.querySelector('.range-info');
        if (rangeInfo) {
            rangeInfo.style.color = '#2c3e50';  // 기본 텍스트 색상으로 복원
        }
    });
    
    // 맨 위로 스크롤
    window.scrollTo({ top: 0, behavior: 'smooth' });
}); 