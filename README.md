# Gemini Discord Bot
這是一個利用 Google 開發的 Gemini 模型的 api 來連接 Discord 機器人的 Chat bot

* 頻道具有黑白名單兩種模式(請見**常見問題**)

* 文字聊天具有短期記憶功能(記憶句數上限可自訂)

* 能夠進行圖片辨識

* 能在DM channel中使用

* 能通過爬蟲簡單理解網址內容

# 前置作業
將需要的機器人設定填入 config.json 中
```
pip install -U -r requirements.txt
```
將 prompt 放入 `Def.py` (可略過) [教學](docs/q3.md)

執行 `main.py`

# 介紹
### [運作原理](docs/principles.md)

### [指令](docs/commands.md)

### [檔案說明](docs/files.md)

### [更新日誌](docs/log.md)

# 常見問題
### [我想要把 channel.json 改成頻道白名單而不是黑名單怎麼辦?](docs/q1.md)

### [如何取得 Gemini api key?](docs/q2.md)

### [如何產生訓練用 prompt?](docs/q3.md)

### [The caller does not have permisson](docs/q4.md)

### [No such file or directory: 'config.json/channel.json'](docs/q5.md)

### [Gemini 不同模型的選擇](docs/q6.md)
