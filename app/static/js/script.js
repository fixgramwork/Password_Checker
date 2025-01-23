async function submitForm(event) {
    event.preventDefault();
    
    const password = document.getElementById('password').value;
    const resultDiv = document.getElementById('result');
    
    try {
        const response = await fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: password
            })
        });
        
        const data = await response.json();
        const result = data.response;
        
        let strengthClass = getStrengthClass(result.strength);
        
        let html = `
            <h3>비밀번호 강도: <span class="${strengthClass}">${result.strength}</span></h3>
            <p>점수: ${result.score}/5</p>
            <h4>피드백:</h4>
            <ul>
                ${result.feedback.map(item => `<li class="feedback-item">${item}</li>`).join('')}
            </ul>
        `;
        
        resultDiv.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<p style="color: red;">오류가 발생했습니다.</p>';
    }
}


function getStrengthClass(strength) {
    switch(strength) {
        case '매우 약함': return 'strength-very-weak';
        case '약함': return 'strength-weak';
        case '보통': return 'strength-medium';
        case '강함': return 'strength-strong';
        case '매우 강함': return 'strength-very-strong';
        default: return '';
    }
}