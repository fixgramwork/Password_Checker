import re
from pathlib import Path
from typing import Dict, List, Union

def check_password_strength(password: str) -> Dict[str, Union[str, int, List[str]]]:
    score = 0
    feedback = []
    
    # 파일 경로 설정
    current_dir = Path(__file__).parent
    common_file = current_dir / 'common.txt'
    
    try:
        with open(common_file, 'r', encoding='utf-8') as f:
            common = f.read().splitlines()
    except FileNotFoundError:
        common = []
        feedback.append("경고: 취약 비밀번호 목록을 불러올 수 없습니다.")

    # 기본 검증
    if not password or len(password.strip()) == 0:
        return {
            "strength": "매우 약함",
            "score": 0,
            "feedback": ["비밀번호를 입력해주세요"]
        }

    # 길이 검사
    if len(password) >= 14:
        score += 1
        feedback.append("비밀번호 길이가 적절합니다.")
    elif len(password) >= 8:
        feedback.append("비밀번호 길이가 최소 기준은 충족하나, 14자 이상을 권장합니다.")
    else:
        feedback.append("비밀번호는 최소 8자 이상이어야 합니다.")

    # 연속된 문자/숫자 패턴 검사
    if re.search(r'(.)\1{2,}', password):
        feedback.append("동일한 문자를 3번 이상 연속해서 사용할 수 없습니다.")
        score -= 1
    
    if re.search(r'(123|234|345|456|567|678|789|987|876|765|654|543|432|321)', password):
        feedback.append("연속된 숫자를 사용할 수 없습니다.")
        score -= 1

    # 대소문자, 숫자, 특수문자 검사
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append("대문자가 포함되어 있습니다.")
    else:
        feedback.append("대문자를 포함하세요.")
    
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append("소문자가 포함되어 있습니다.")
    else:
        feedback.append("소문자를 포함하세요.")
    
    if re.search(r"\d", password):
        score += 1
        feedback.append("숫자가 포함되어 있습니다.")
    else:
        feedback.append("숫자를 포함하세요.")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>+\-_=~`[\]\\;'/]", password):
        score += 1
        feedback.append("특수문자가 포함되어 있습니다.")
    else:
        feedback.append("특수문자를 포함하세요.")

    # 흔한 비밀번호 검사
    if password in common:
        feedback.append("흔히 사용되는 취약한 비밀번호입니다.")
        score = 0

    # 점수 보정
    score = max(0, min(score, 5))  # 점수를 0-5 사이로 제한

    return {
        "strength": get_strength_level(score),
        "score": score,
        "feedback": feedback
    }

def get_strength_level(score: int) -> str:
    strength_levels = {
        0: "매우 약함",
        1: "매우 약함",
        2: "약함",
        3: "보통",
        4: "강함",
        5: "매우 강함"
    }
    return strength_levels.get(score, "매우 약함")