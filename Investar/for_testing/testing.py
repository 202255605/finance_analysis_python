import requests  # pip install requests

code = 68270

try:
    url = f"http://finance.naver.com/item/sise_day.nhn?code={code}" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = 'euc-kr'  # 명시적으로 euc-kr 설정
    doc = response.text

    print(doc)
    
    print("데이터 로딩 성공")
    
except Exception as e:
    print(f"에러 발생: {e}")
