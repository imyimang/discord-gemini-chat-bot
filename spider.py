import requests, re
from bs4 import BeautifulSoup

def gettitle(website_url: str) -> str | None:
    '''
    取得網頁的 title 標籤並回傳
    '''
    try:
        response = requests.get(website_url) # 發送 GET 請求

        soup = BeautifulSoup(response.text, 'html.parser') # 使用 BeautifulSoup 解析 HTML

        print(f'The title of the website is: {soup.title.string}') # 印出 title
        return soup.title.string
    
    except Exception:
        return None

def islink(content: str) -> str: # 判定訊息是否是連結
    return re.findall(r'https?://\S+', content) # 如果是連結就返回連結 + 連結以外的文字