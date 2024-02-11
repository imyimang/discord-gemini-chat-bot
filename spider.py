import requests
from bs4 import BeautifulSoup
import re


def gettitle(website_url):
    

    try:
        # 發送GET請求
        response = requests.get(website_url)

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 獲取<title>標籤的內容
        title = soup.title.string

        # 印出title
        print(f"The title of the website is: {title}")
        return title
    except Exception as e:
        return None
    
#判定訊息是否是連結
def islink(content):
    return re.findall(r'https?://\S+', content)    
#如果是連結就返回連結+連結以外的文字