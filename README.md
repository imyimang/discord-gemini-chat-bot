# Gemini Discord Bot
[![Python](https://img.shields.io/badge/python-%3E%3D%203.12-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.4.0-blue)](https://github.com/Rapptz/discord.py)
[![Stars](https://img.shields.io/github/stars/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/stargazers)
[![Forks](https://img.shields.io/github/forks/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/forks)
[![License](https://img.shields.io/github/license/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/blob/main/LICENSE)

## [English](README_EN.md) | 繁體中文 

這是一個利用 Google Gemini 模型的 API 來製作的 Discord AI 聊天機器人

* 具有短期記憶功能(記憶句數上限可自訂)

* 能夠進行圖片辨識

* 能在 DM 中使用

* 能通過爬蟲簡單理解網址內容

## 安裝
將機器人設定填入 `.env.example` 中，然後將它重新命名為 `.env`

安裝函式庫:
```powershell
pip install -U -r requirements.txt
```
將 prompt 放入 `call_api.py` (可略過) [教學](docs/zh/q7.md)

將 history 放入 `call_api.py` (可略過) [教學](docs/zh/q3.md)

執行 `main.py`

## 介紹
- [運作原理](docs/zh/principles.md)
- [指令](docs/zh/commands.md)
- [更新日誌](docs/zh/log.md)

## 常見問題
- [如何取得 Gemini API key?](docs/zh/q2.md)
- [如何撰寫提示詞?](docs/zh/q7.md)
- [如何產生訓練用的history?](docs/zh/q3.md)
- [Error:The caller does not have permisson](docs/zh/q4.md)
- [Error:No such file or directory: 'config.json/channel.json'](docs/zh/q5.md)
- [Gemini 不同模型的選擇](docs/zh/q6.md)


# 參考資料
- [Echoshard/Gemini_Discordbot](https://github.com/Echoshard/Gemini_Discordbot)
- [peter995peter/discord-gemini-ai](https://github.com/peter995peter/discord-gemini-ai)