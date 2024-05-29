# Gemini Discord Bot

## English | [繁體中文](README.md) 

This is a  Discord chat bot that using an API from Google's Gemini model.

* It has two modes: whitelist and blacklist.(See the **FAQ** for more details)

* The text chat includes short-term memory functionality, with the option to customize the maximum number of sentences it can remember.

* It's capable of performing image recognition.

* It can be used in DM (Direct Message) channels.

* It can understand website content through web scraping.

# Get Started
Fill in the required bot settings in `config.json`.
```
pip install -U -r requirements.txt
```
Put prompt in `Def.py` (Skippable) [Tutorial](docs/en/q3_en.md)

Run `main.py`

# Project introduction
### [Operating principle](docs/en/principles_en.md)

### [commands](docs/en/commands_en.md)

### [File introduction](docs/en/files_en.md)

### [Development log](docs/en/log_en.md)

# FQA
### [How to change mode from blacklist to whitelist](docs/en/q1_en.md)

### [How to get Gemini api key](docs/en/q2_en.md)

### [How to generate prompts for training](docs/en/q3_en.md)

### [Error:The caller does not have permisson](docs/en/q4_en.md)

### [Error:No such file or directory: 'config.json/channel.json'](docs/en/q5_en.md)

### [Choosing between different models in Gemini](docs/en/q6_en.md)


# Reference
### [Echoshard/Gemini_Discordbot](https://github.com/Echoshard/Gemini_Discordbot)

### [peter995peter/discord-gemini-ai](https://github.com/peter995peter/discord-gemini-ai)