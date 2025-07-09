import time

# 미리 정해놓은 조-장소 매칭 (조작 가능)
ladder_result = {
    '1조': 'D',
    '2조': 'A',
    '3조': 'B',
    '4조': 'B',
    '5조': 'E',
    '6조': 'A',
    '7조': 'C',
    '8조': 'E'
}

# 사다리 타기 진행 애니메이션 효과 함수
def ladder_simulator():
    print("🎉 사다리 타기 게임을 시작합니다! 🎉\n")
    for team in ladder_result.keys():
        input(f"'{team}' 사다리를 타려면 엔터를 눌러주세요...")
        print(f"{team} 사다리 진행중...", end='', flush=True)
        
        # 간단한 사다리 진행 느낌 연출 (점점 출력)
        steps = ['│', '─', '│', '─', '│', '─', '│']
        for step in steps:
            print(step, end='', flush=True)
            time.sleep(0.3)
        print(f" → {ladder_result[team]} 도착!\n")
        time.sleep(0.5)
        
    print("모든 사다리 결과가 완료되었습니다! 감사합니다 😊")

if __name__ == "__main__":
    ladder_simulator()
