import chardet

with open('DBUpdater.py', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    print(f"파일 인코딩: {result['encoding']}")
