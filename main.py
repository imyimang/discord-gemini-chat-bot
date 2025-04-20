import discord
from discord.ext import commands, tasks
import re, json, aiohttp, os
import aiofiles
from itertools import cycle
from dotenv import load_dotenv
from call_api import prompt, text_api, image_api
from spider import islink, gettitle
from tools import wolframalpha,get_news,youtube_search

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")
MODE = os.getenv("MODE", "whitelist")
MEMORY_MAX = int(os.getenv("MEMORY_MAX", 100))

# Functions
# ==================================================
def update_message_history(channel_id: int, text: str) -> str:
    if channel_id not in log:
        log[channel_id] = []
    log[channel_id].append(text)
    if len(log[channel_id]) > MEMORY_MAX:
        log[channel_id].pop(0)
    return "\n".join(log[channel_id])

def format_discord_message(input_string: str) -> str:
    '''
    刪除並回傳 Discord 聊天訊息中位於 < 和 > 之間的文字 (讓他能夠放入短期記憶並被 AI 讀懂)
    '''
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

def get_message_history(channel_id: int) -> str | None:
    '''
    回傳指定頻道的短期記憶
    '''
    if channel_id in log: # 如果 channel_id 有在 log 字典裏面
        return '\n\n'.join(log[channel_id])

def load_channel_data(channel: discord.abc.GuildChannel) -> tuple[str, list]:
    '''
    讀取並回傳資料
    '''
    with open('channel.json', 'r', encoding='utf-8') as file: # 打開 json 檔案
        data: dict = json.load(file)

    if 'id' not in data:
        data['id'] = []
        save_data(data, "channel")

    channel_list: list = data['id'] # 定義 channel_list 為 json 裡面鍵值為 'id' 的資料

    return str(channel.id), channel_list, data

def save_data(data: dict, data_file: str):
    '''
    儲存檔案
    '''
    with open(f'{data_file}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def extract_json_block(text):
    """
    從文字中尋找並解析第一個合法的 JSON 區塊（支援巢狀），
    返回 (解析後的 JSON 物件, 起始位置, 結束位置) 或 None。
    """
    start = text.find("{")
    while start != -1:
        stack = []
        for i in range(start, len(text)):
            if text[i] == "{":
                stack.append("{")
            elif text[i] == "}":
                if stack:
                    stack.pop()
                if not stack:  # 找到完整的 JSON 區塊
                    json_str = text[start:i+1]
                    try:
                        parsed_json = json.loads(json_str)
                        return parsed_json, start, i + 1
                    except json.JSONDecodeError:
                        break  # JSON 格式錯誤，換下一組
        start = text.find("{", start + 1)
    return None, -1, -1

async def process_tools_in_response(channel_id: int, response: str) -> str:
    print("原始回應：", response)
    all_tool_outputs = []  # 儲存所有工具的執行結果
    processed_jsons = set()  # 記錄已處理的 JSON 字符串，避免重複
    max_iterations = 20  # 限制最大迭代次數，防止無限循環

    iteration = 0
    while iteration < max_iterations:
        data, start, end = extract_json_block(response)
        if not data:
            print("未找到新的 JSON 區塊，結束提取")
            break

        # 將 JSON 轉為字符串，用於檢查是否已處理
        json_str = json.dumps(data, sort_keys=True)
        if json_str in processed_jsons:
            print(f"檢測到重複的 JSON 區塊：{json_str}，跳過")
            # 移除重複的 JSON 區塊，防止下次循環再次提取
            response = response[:start] + response[end:]
            iteration += 1
            continue

        tool_response = None
        if data.get("type") == "wolframalpha" and data.get("question_original") and data.get("question_english"):
            print(f"正在使用 wolframalpha，內容原文:{data["question_original"]}，內容英文:{data["question_english"]}")
            tool_response = wolframalpha(data["question_english"], data["question_original"])

        elif data.get("type") == "get_news" and data.get("category"):
            print(f"正在使用 get_news，類別：{data['category']}")
            tool_response = get_news(data["category"])

        elif data.get("type") == "youtube_search" and data.get("query") and data.get("max_results") and data.get("language") and data.get("duration"):
            print(f"正在使用 youtube_search，內容：{data['query']}")
            tool_response = await youtube_search(data["query"], int(data["max_results"]), data["language"], data["duration"])

        # 移除當前 JSON 區塊（無論是否有有效工具回應）
        response = response[:start] + response[end:]
        print("移除 JSON 後的回應：", response)

        if tool_response:
            print("工具結果：", tool_response)
            all_tool_outputs.append(tool_response)
            processed_jsons.add(json_str)  # 記錄已處理的 JSON
        else:
            print(f"無效工具或缺少參數，跳過 JSON：{json_str}")
            processed_jsons.add(json_str)  # 即使無效也要記錄，避免重複處理

        iteration += 1

    # 如果有工具結果，則一次性送回模型處理
    if all_tool_outputs:
        print("所有工具結果：", all_tool_outputs)
        # 將工具結果合併到系統提示中，並明確要求模型不要生成新的工具 JSON
        history = update_message_history(
            channel_id,
            "[system]: (模型已調用外部工具，結果如下，請根據結果回應使用者的問題，並避免生成新的工具 JSON 區塊)\n" +
            "\n".join(all_tool_outputs)
        )
        response = await text_api(prompt +  history)
        update_message_history(channel_id, "[model]: " + response)
    else:
        print("無工具結果，直接返回原始回應")

    return response
# ==================================================

log: dict[int, list[str]] = {} # 創建一個名稱叫 log 的字典, 用來存放短期記憶

# 檢查 MODE 是否有效
while True:
    if MODE in ['whitelist', 'blacklist']: break
    MODE = input('不明的模式，模式應為 "whitelist" 或 "blacklist"\n輸入執行模式: ')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), intents=discord.Intents.all())

status = cycle(['Gemini chat bot', '我是 AI 機器人', '正在聊天']) # 機器人顯示的個人狀態,可自行更改

@tasks.loop(seconds=10) # 每隔 10 秒更換一次機器人個人狀態
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_ready():
    print(f'{bot.user} 已上線，正在執行 {"白名單" if MODE == "whitelist" else "黑名單"} 模式！')
    change_status.start() # 讓機器人顯示狀態

# Commands
# ==================================================
if MODE == 'whitelist':
    @bot.command()
    @commands.guild_only()
    async def openchannel(ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        '''
        新增白名單內頻道
        '''
        channel = channel or ctx.channel

        channel_id, channel_list, data = load_channel_data(channel)

        if channel_id not in channel_list: # 如果頻道 id 未被記錄在 json 檔案
            channel_list.append(channel_id) # 新增 channel_id 這筆資料

            data['id'] = channel_list
            save_data(data, "channel")

        await ctx.reply('頻道已成功開啟 AI 聊天。', mention_author=False)

    @bot.command()
    @commands.guild_only()
    async def closechannel(ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        '''
        移除白名單內頻道
        '''
        channel = channel or ctx.channel

        channel_id, channel_list, data = load_channel_data(channel)

        if channel_id in channel_list: # 如果頻道 id 已被記錄在 json 檔案
            channel_list.remove(channel_id) # 移除 channel_id 這筆資料

            data['id'] = channel_list
            save_data(data, "channel")

        await ctx.reply('頻道已成功關閉 AI 聊天。', mention_author=False)

elif MODE == "blacklist":
    @bot.command()
    @commands.guild_only()
    async def blockchannel(ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        '''
        新增黑名單內頻道
        '''
        channel = channel or ctx.channel

        channel_id, channel_list, data = load_channel_data(channel)

        if channel_id not in channel_list: # 如果頻道 id 未被記錄在 json 檔案
            channel_list.append(channel_id) # 新增 channel_id 這筆資料

            data['id'] = channel_list
            save_data(data, "channel")

        await ctx.reply('頻道已成功屏蔽。', mention_author=False)
    
    @bot.command()
    @commands.guild_only()
    async def unblockchannel(ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        '''
        移除黑名單內頻道
        '''
        channel = channel or ctx.channel

        channel_id, channel_list, data = load_channel_data(channel)

        if channel_id in channel_list: # 如果頻道 id 已被記錄在 json 檔案
            channel_list.remove(channel_id) # 移除 channel_id 這筆資料

            data['id'] = channel_list
            save_data(data, "channel")

        await ctx.reply('頻道已成功解除屏蔽。', mention_author=False)

@bot.command()
async def reset(ctx: commands.Context, channel: discord.abc.Messageable = None):
    '''
    清空頻道短期記憶
    '''
    channel = channel or ctx.channel

    if channel.id in log:
        del log[channel.id] # 清空短期記憶
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.reply(f'{channel.mention} 的短期記憶已清空。', mention_author=False)
        else:
            await ctx.reply(f'本私訊的短期記憶已清空。', mention_author=False)
    else:
        await ctx.reply('並無儲存的短期記憶。', mention_author=False)
# ==================================================        

import os

@bot.listen('on_message')
async def handle_message(msg: discord.Message):
    if msg.author == bot.user:
        return

    command_name = msg.content.removeprefix(PREFIX)
    if (command_name in [cmd.name for cmd in bot.commands]):
        return

    if not isinstance(msg.channel, discord.DMChannel):
        can_send = msg.channel.permissions_for(msg.guild.me).send_messages
        if not can_send:
            print(f'沒有權限在此頻道 ({msg.channel.name}) 發言。')
            return 

    result = load_channel_data(msg.channel)
    channel_id, channel_list = result[0], result[1]
    if ((MODE == 'whitelist' and channel_id not in channel_list) or 
        (MODE == 'blacklist' and channel_id in channel_list)) and not isinstance(msg.channel, discord.DMChannel):
        return

    async with msg.channel.typing():
        attachment_info = None

        # 處理圖片與文字檔附件
        if msg.attachments:
            for attachment in msg.attachments:
                filename = attachment.filename.lower()

                # 圖片處理
                if any(filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                await msg.reply('圖片載入失敗。', mention_author=False)
                                return
                            print(f'正在分析 {msg.author.name} 的圖片...')
                            image_data = await resp.read()
                            response_text = await image_api(image_data)
                            attachment_info = f"(附上一張圖片，內容是「{response_text}」)"

                # 純文字檔處理
                elif any(filename.endswith(ext) for ext in ['.txt', '.md', '.log']):
                    file_path = f"temp_{msg.id}_{filename}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                await msg.reply('文字檔案載入失敗。', mention_author=False)
                                return
                            f = await aiofiles.open(file_path, mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                    try:
                        f = await aiofiles.open(file_path, mode='r', encoding='utf-8', errors='ignore')
                        text_data = await f.read()
                        await f.close()
                        print(f'使用者上傳的文字檔內容:\n{text_data[:500]}')
                        attachment_info = f"(附上一個文字檔，內容是「{text_data[:300]}...」)"
                    finally:
                        if os.path.exists(file_path):
                            os.remove(file_path)

        # 處理網址
        word = msg.content
        links = islink(msg.content)
        if links:
            for link in links:
                title = gettitle(link)
                word = word.replace(link, f'(一個網址, 網址標題是: "{title}")\n' if title else '(一個網址, 網址無法辨識)\n')

        if attachment_info:
            word += f"\n{attachment_info}"

        dc_msg = format_discord_message(word)
        update_message_history(msg.channel.id, f"[{msg.author.name}]:{dc_msg}")
        reply_text = await text_api(prompt + get_message_history(msg.channel.id))

        # 根據環境變數決定是否要處理工具
        if os.getenv("CALL_TOOLS", "false").lower() == "true":
            reply_text = await process_tools_in_response(msg.channel.id, reply_text)

        await msg.reply(reply_text.replace("[model]:", ""), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        update_message_history(msg.channel.id, f"[model]:" + reply_text)

        # 除錯印出
        print(f'Server name: {msg.guild.name if not isinstance(msg.channel, discord.DMChannel) else "私訊"}')
        print(f'Message ID: {msg.id}')
        print(f'Message Content: {msg.content}')
        print(f'Author ID: {msg.author.id}')
        print(f'Author Name: {msg.author.name}')
        if not isinstance(msg.channel, discord.DMChannel):
            print(f'Channel name: {msg.channel.name}')
            print(f'Channel id: {msg.channel.id}')
        print("附件摘要:", attachment_info)
        print("模型回覆:\n", reply_text)

bot.run(TOKEN)