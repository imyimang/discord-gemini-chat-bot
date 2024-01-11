
import google.generativeai as genai #導入函式庫


genai.configure(api_key="you api key") #中間放上你的api key 如果不知道怎麼拿api key請看文檔

# 模型設定 詳細設定請去google
generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
# 安全設定 建議可以照著下面的
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "block_none"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "block_none"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "block_none"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "block_none"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings) #設定模型 這邊不用動他

convo = model.start_chat(history=[
 # 這裡放你的prompt
])

async def history(msg): #建立一個副函式

        
    await convo.send_message_async(msg) #傳送msg內容給gemini api
    print(f":{convo.last.text}") #print出api的回應(可省略)
    reply_text = convo.last.text 
    return reply_text #將api的回應返還給主程式
