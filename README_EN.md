# Gemini Discord Bot
[![Python](https://img.shields.io/badge/python-%3E%3D%203.12-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-%3E%3D%202.4.0-blue)](https://github.com/Rapptz/discord.py)
[![Stars](https://img.shields.io/github/stars/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/stargazers)
[![Forks](https://img.shields.io/github/forks/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/forks)
[![License](https://img.shields.io/github/license/imyimang/discord-gemini-chat-bot)](https://github.com/imyimang/discord-gemini-chat-bot/blob/main/LICENSE)

## English | [繁體中文](README.md)

This is a Discord AI chatbot created using the Google Gemini model's API.

* Have a short-term memory function (memory sentence limit is customizable).

* It can perform image recognition.

* It can be used in DM.

* It can understand the content of URLs through web crawling.

## Demo
<details>
  <summary>Click here</summary>
  <img src="docs/images/14.jpg" alt="Image">
</details>

## Installation
Fill in the bot settings in `.env.example`, then rename it to `.env`.

Install libraries:
```powershell
pip install -U -r requirements.txt
```
Place the prompt in `call_api.py` (optional) [Tutorial](docs/en/q7_en.md)

Place the history in `call_api.py` (optional) [Tutorial](docs/en/q3_en.md)

Run `main.py`

## Introduction
- [How it works](docs/en/principles_en.md)
- [Commands](docs/en/commands_en.md)
- [Changelog](docs/en/log_en.md)

## FAQ
- [How to get a Gemini API key?](docs/en/q2_en.md)
- [How to write prompts?](docs/en/q7_en.md)
- [How to generate training history?](docs/en/q3_en.md)
- [Error: The caller does not have permission](docs/en/q4_en.md)
- [Error: No such file or directory: 'config.json/channel.json'](docs/en/q5_en.md)
- [Different Gemini model options](docs/en/q6_en.md)

# References
- [Echoshard/Gemini_Discordbot](https://github.com/Echoshard/Gemini_Discordbot)
- [peter995peter/discord-gemini-ai](https://github.com/peter995peter/discord-gemini-ai)