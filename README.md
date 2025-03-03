# 📈 ETF 자동매매 시스템 🤖

이 프로젝트는 대신증권의 크레온 API를 활용한 ETF 자동매매 시스템입니다. 파이썬으로 구현되었으며, 특정 매매 전략에 따라 ETF를 자동으로 매수/매도하는 기능을 제공합니다.

![Python](https://img.shields.io/badge/Python-3.8-blue)
![Creon API](https://img.shields.io/badge/Creon-API-orange)
![Stock](https://img.shields.io/badge/Stock-ETF-green)

## ✨ 주요 기능

- 🔄 크레온 API 자동 연결
- 🔍 ETF 종목 정보 스크래핑
- 💹 설정된 매매 전략에 따른 자동 매매
- 📱 슬랙을 통한 매매 알림

## 📁 파일 구조

- `ch08_01_AutoConnect.py`: 크레온 API 자동 연결 스크립트
- `ch08_02_DynamicPageScraping_NaverETF.py`: 네이버 금융에서 ETF 정보 스크래핑
- `confirmation_check.py`: 크레온 시스템 연결 상태 확인
- `EtfAlgoTrader.py`: 메인 트레이딩 알고리즘

## 🔧 요구사항

### 📦 패키지 의존성
- pywinauto
- win32com.client
- selenium
- bs4 (BeautifulSoup)
- pandas
- slack_sdk

### 🌐 외부 요구사항
- 대신증권 크레온 플러스 설치 (CREON PLUS)
- 크레온 API 사용 가능한 계정
- Chrome 웹 브라우저 및 chromedriver
- 슬랙 API 토큰 (알림 기능 사용시)

## 💿 설치 방법

1. 필요한 패키지 설치
```bash
pip install pywinauto selenium beautifulsoup4 pandas slack_sdk pywin32
```

2. chromedriver 설치
   - 🌐 Chrome 버전에 맞는 chromedriver를 다운로드하여 `C:\myPackage\chromedriver.exe` 경로에 저장

3. 크레온 API 설정
   - 🏢 대신증권 홈페이지에서 CREON PLUS 다운로드 및 설치
   - 🔐 로그인 정보 설정

## 🚀 사용 방법

### 1. 크레온 API 자동 연결
```bash
python ch08_01_AutoConnect.py
```
- ⚠️ 사용 전 크레온 아이디, 비밀번호, 공인인증서 비밀번호를 스크립트에 설정해야 함

### 2. ETF 목록 스크래핑
```bash
python ch08_02_DynamicPageScraping_NaverETF.py
```

### 3. 크레온 연결 상태 확인
```bash
python confirmation_check.py
```

### 4. 자동 매매 실행
```bash
python EtfAlgoTrader.py
```

## 📊 트레이딩 전략

본 시스템은 다음과 같은 매매 전략을 사용합니다:

1. ⏰ 매일 오전 9:05에 보유 종목 전량 매도
2. 💰 오전 9:05부터 오후 3:15 사이에 매수 조건 충족 시 매수
   - 현재가 > 목표가
   - 현재가 > 5일 이동평균선
   - 현재가 > 10일 이동평균선
3. 💸 오후 3:15부터 오후 3:20 사이에 보유 종목 전량 매도
4. 🔚 오후 3:20 이후 프로그램 종료

## ⚠️ 주의사항

- 👨‍💻 관리자 권한으로 실행해야 함
- 🪟 크레온 API는 윈도우 환경에서만 동작
- 💬 슬랙 알림을 사용하려면 유효한 슬랙 API 토큰이 필요
- 💼 실제 투자에 사용 시 충분한 테스트와 검증이 필요
- 🐍 Python 3.8.0 버전과 pywin32 라이브러리 간 충돌이 발생할 수 있음

## ⚙️ 커스터마이징

- `symbol_list`: 트레이딩할 ETF 종목 코드 수정
- `target_buy_count`: 동시에 보유할 최대 종목 수 설정
- `buy_percent`: 매수에 사용할 자금 비율 설정
- 매수/매도 시간 설정 변경 가능

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 🙏 기여

기여는 언제나 환영합니다! 이슈를 제기하거나 Pull Request를 보내주세요.

## 📧 연락처

질문이나 피드백이 있으시면 언제든지 연락주세요.

---

### 💡 성공적인 투자를 기원합니다! 📈
