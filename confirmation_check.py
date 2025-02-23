import os, sys, ctypes # CTYPES라이브러리는 파이썬에서 c타입의 자료형을 사용하거나 윈도우에 설치된 dll모듈을 호출할때 사용하는 라이브러리 이다.(DLL = dynamic link library)
import win32com.client # 크레온 api에서 제공하는 COM오브젝트를 사용하려면 파이윈32라이브러리가 필요하다

cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')

def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_system() : admin user -> FAILED')
        return False
 
    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        print('check_creon_system() : connect to server -> FAILED')
        return False
 
    # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    if (cpTradeUtil.TradeInit(0) != 0):
        print('check_creon_system() : init trade -> FAILED')
        return False
    return True

if __name__ == '__main__': 
    confirmation = check_creon_system()
    print(confirmation)

    # 와 씨발 연결됐어 이거 진짜 가상환경에 설치하기도 했고 pywin32 라는 라이브러리와 python3.8.0.버전간의 충돌이 가장 큰 듯
    # 그니까 멀쩡한 라이브러리 잘 import해와도 작동 하나도 안 되고 애초에 불러 지지도 않음 그리고 