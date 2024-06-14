
import google.generativeai as genai
import json

data = json.load(open('config.json', encoding='utf-8'))
genai.configure(api_key=data['api_key'])

# 模型設定, 詳細設定請去 Google
generation_config = {
    'temperature': 1,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048,
}

# 安全設定, 建議可以照著下面的
safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'block_none'
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'block_none'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'block_none'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'block_none'
    },
]

model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config=generation_config, safety_settings=safety_settings) # 設定模型, 這邊不用動他

image_model = genai.GenerativeModel(model_name='gemini-pro-vision', generation_config=generation_config, safety_settings=safety_settings) # 定義另外一個 model 用來生成圖片回應 (兩者不能相容)

#==============================================================

async def text_api(msg: str) -> str | None:
    '''
    呼叫 api 並回傳他的回應
    '''
    convo = model.start_chat(history=[
        # 這裡放你的 prompt
    ])

    if not msg:return '這段訊息是空的'

    await convo.send_message_async(msg) # 傳送 msg 內容給 Gemini api
    reply_text = convo.last.text
    print(f': {reply_text}') # print 出 api 的回應 (可省略)
    return reply_text # 將 api 的回應返還給主程式

async def image_api(image_data, text: str) -> str:
    '''
    回傳 api 對包含圖片的訊息的回應
    '''
    image_parts = [{'mime_type': 'image/jpeg', 'data': image_data}]

    # (下) 如果 text 不為空, 就用 text 依據文字內容來生成回應, 如果為空, 就依據 '這張圖片代表什麼?給我更多細節' 來生成回應
    prompt_parts = [image_parts[0], f'\n{text if text else "這張圖片代表什麼? 給我更多細節"}']
    response = image_model.generate_content(prompt_parts)

    if response._error:return '無法分析這張圖'

    return response.text