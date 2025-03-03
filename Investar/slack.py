from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 봇 토큰으로 클라이언트 초기화
client = WebClient(token='[내 slack token]')

try:
    # 메시지 포맅팅 
    markdown_text = '''
    This message is plain.
    *This message is bold.*
    `This message is code.`
    *This message is italic.*
    ~This message is strike.~
    '''

    # 첨부파일 설정
    attach_dict = {
        'color': '#ff0000',
        'author_name': 'INVESTAR',
        'author_link': 'github.com/investar',
        'title': '오늘의 증시 KOSPI',
        'title_link': 'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
        'text': '2,326.13 △11.89 (+0.51%)',
        'attachments': [
        {
            'image_url': 'https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png',
            'alt_text': 'KOSPI Chart'
        }
    ]
    }

    # Slack API 호출
    response = client.chat_postMessage(
        channel="#notgeneral",
        text=markdown_text,
        attachments=[attach_dict]
    )
    print('끝')

except SlackApiError as e:
    print(f"Error: {e.response['error']}")
