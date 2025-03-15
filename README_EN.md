# Gemini Discord Bot

## English | [繁體中文](README.md)

This is a Discord AI chatbot created using the Google Gemini model's API.

* Channels have two modes: blacklist and whitelist (please see [**FAQ**](#faq)).

* Text chat has a short-term memory function (memory sentence limit is customizable).

* It can perform image recognition.

* It can be used in DM channels.

* It can understand the content of URLs through web crawling.

## Deployment
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
- [File description](docs/en/files_en.md)
- [Changelog](docs/en/log_en.md)

## FAQ
- [How can I change channel.json to a whitelist instead of a blacklist?](docs/en/q1_en.md)
- [How to get a Gemini API key?](docs/en/q2_en.md)
- [How to write prompts?](docs/en/q7_en.md)
- [How to generate training history?](docs/en/q3_en.md)
- [Error: The caller does not have permission](docs/en/q4_en.md)
- [Error: No such file or directory: 'config.json/channel.json'](docs/en/q5_en.md)
- [Different Gemini model options](docs/en/q6_en.md)

# References
- [Echoshard/Gemini_Discordbot](https://github.com/Echoshard/Gemini_Discordbot)
- [peter995peter/discord-gemini-ai](https://github.com/peter995peter/discord-gemini-ai)