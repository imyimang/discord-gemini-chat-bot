這是一個利用google開發的gemini模型的api來連接discord機器人的Chat bot

* 頻道具有黑白名單兩種模式(請見**常見問題**)

* 文字聊天具有短期記憶功能(記憶句數上限可自訂)

* 能夠進行圖片辨識

* 能在DM channel中使用

* 能通過爬蟲簡單理解網址內容

# 前置作業
將需要的機器人設定填入config.json中
```
pip install -U -r requirements.txt
```

# 介紹
### [運作原理](docs/principles.md)

### [指令](docs/commands.md)

# 常見問題
### [我想要把channel.json改成頻道白名單而不是黑名單怎麼麼辦](docs/q1.md)

### [如何取得gemini api key](docs/q2.md)

### [如何產生訓練prompt](docs/q3.md)

### [The caller does not have permisson](docs/q4.md)

### [No such file or directory: 'config.json/channel.json'](docs/q5.md)

### [Gemini不同模型的選擇](docs/q6.md)











