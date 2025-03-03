# 📈 주식 시장 분석 및 투자 전략 도구 🚀

<div align="center">
  
  ![Finance Analytics](https://img.shields.io/badge/Finance-Analytics-blue)
  ![Python](https://img.shields.io/badge/Python-3.7+-green)
  ![MariaDB](https://img.shields.io/badge/Database-MariaDB-orange)
  
</div>

## 🌟 프로젝트 소개

이 프로젝트는 한국 주식 시장 데이터를 수집하고 분석하여 다양한 투자 전략과 시각화 도구를 제공합니다. 효율적 투자선, 볼린저 밴드, 삼중 스크린 거래 시스템 등 다양한 기술적 분석 방법론을 구현했습니다.

---

## ✨ 주요 기능

- 🔄 한국 주식 시장 데이터 자동 수집 및 데이터베이스 저장
- 📊 효율적 투자선(Efficient Frontier) 계산 및 시각화
- 📉 볼린저 밴드(Bollinger Band) 분석
- 🔍 삼중 스크린 거래 시스템(Triple Screen Trading System) 구현
- 🧪 Backtrader를 활용한 거래 전략 백테스팅

---

## 📂 파일 설명

### 📥 데이터 수집 및 관리

- **DBUpdater.py**: 네이버 금융에서 주식 데이터를 수집하여 MariaDB에 저장하는 모듈
- **MarketDB_codes_date_updated_final.py**: 데이터베이스에서 주식 데이터를 가져오는 API 클래스
- **marketDB_only_by_codes.py**: 코드를 기반으로 주식 정보를 가져오는 간소화된 API
- **config.json**: 데이터 수집 설정 파일

### 💼 포트폴리오 최적화

- **ch06_01_Efficient_Frontier_line.py**: 효율적 투자선을 계산하고 시각화
- **ch06_02_PoerfolioOptimization.py**: 샤프 비율을 기반으로 한 포트폴리오 최적화

### 📊 볼린저 밴드 분석

- **ch06_03_BollingerBand.py**: 기본 볼린저 밴드 구현
- **ch06_04_BollingerBand_PercentB.py**: 볼린저 밴드와 %B 지표
- **ch06_05_BollingerBand_BandWidth.py**: 볼린저 밴드와 밴드폭 지표
- **ch06_06_BollingerBand_TrendFollowing.py**: 볼린저 밴드를 이용한 추세 추종 전략
- **ch06_07_BollingerBand_IIP21.py**: 볼린저 밴드와 내부강도지수(II%) 지표
- **ch06_08_BollingerBand_Reversals.py**: 볼린저 밴드를 이용한 반전 신호 포착

### 🔎 삼중 스크린 거래 시스템

- **ch06_09_FirstScreen.py**: 삼중 스크린 거래 시스템의 첫 번째 화면(주간 추세)
- **ch06_10_SecondScreen.py**: 삼중 스크린 거래 시스템의 두 번째 화면(일간 반전)
- **ch06_11_TripleScreen.py**: 완전한 삼중 스크린 거래 시스템 구현
- **ch06_11_TripleScreen_recovering_fucking_result.py**: 수정된 삼중 스크린 거래 시스템

### 🧮 백테스팅

- **ch07_09_Backtrader_RSI_SMA.py**: Backtrader 라이브러리를 이용한 RSI 및 SMA 전략 백테스팅

### 🔔 알림 기능

- **slack.py**: Slack을 이용한 주식 시장 알림 기능

---

## 🚀 설치 및 설정

### 📦 필수 라이브러리

```bash
pip install pandas numpy matplotlib pymysql beautifulsoup4 backtrader yfinance mpl_finance slack_sdk
```

### 🗄️ 데이터베이스 설정

MariaDB를 설치하고 다음과 같이 설정합니다:

1. 데이터베이스 생성: `CREATE DATABASE INVESTAR;`
2. 사용자 설정: 코드 내의 데이터베이스 연결 정보를 자신의 환경에 맞게 수정

### 💻 기본 사용법

1. 데이터 수집 실행:
   ```python
   python DBUpdater.py
   ```

2. 분석 예시 - 효율적 투자선:
   ```python
   python ch06_01_Efficient_Frontier_line.py
   ```

3. 분석 예시 - 볼린저 밴드:
   ```python
   python ch06_03_BollingerBand.py
   ```

---

## 📋 분석 결과 예시

<div align="center">
  
  | 분석 도구 | 설명 |
  |----------|------|
  | 📈 효율적 투자선 | 최적의 리스크-리턴 비율을 가진 포트폴리오 구성 |
  | 📊 볼린저 밴드 | 가격 변동성을 기반으로 한 기술적 분석 도구 |
  | 🔍 삼중 스크린 | 장기, 중기, 단기 추세를 모두 고려한 거래 시스템 |
  | 📉 백테스팅 | 과거 데이터로 투자 전략의 성과 테스트 |
  
</div>

---

## ⚠️ 참고사항

- 🔄 이 프로젝트는 네이버 금융 데이터를 크롤링하므로 네이버의 정책 변경에 따라 작동이 중단될 수 있습니다.
- 🧪 실제 투자에 사용하기 전에 충분한 백테스팅과 검증이 필요합니다.
- 🔔 Slack 알림 기능을 사용하려면 `slack.py` 파일에 유효한 Slack API 토큰을 설정해야 합니다.

---


<div align="center">
  
  ### 💹 행복한 투자되세요! 💰
  
</div>
