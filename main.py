# 如果你想要看懂整個程式
# 建議去科普一下 json 檔, Python 字典, Python 函式的運作原理

import discord
from discord.ext import commands, tasks
import re, json, aiohttp
from itertools import cycle
from call_api import prompt, text_api, image_api
from spider import islink, gettitle # 從 call_api.py 和 spider.py 中導入函式

# ==================================================

def update_message_history(channel_id: int, text: str) -> None:
    '''
    更新短期記憶
    '''
    if channel_id not in log: log[channel_id] = [] # 如果 channle_id 不在在字典裡面則創建
    log[channel_id].append(text) # 把 text 加入以 channle_id 命名的鍵中

    if len(log[channel_id]) > int(config_data['memory_max']): # 如果 channle_id 裡面存的資料大於 config 中的記憶上限
        log[channel_id].pop(0) # 就 pop 最早的一筆資料

def format_discord_message(input_string: str) -> str:
    '''
    刪除並回傳 Disord 聊天訊息中位於 < 和 > 之間的文字 (讓他能夠放入短期記憶並被 AI 讀懂)
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

async def split_and_edit_message(msg: discord.Message, bot_msg: discord.Message, text: str, max_length: int) -> None:
    '''
    拆分並編輯訊息
    '''
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i:i+max_length] # 如果訊息長度超過 max_length 就把他拆開
        messages.append(sub_message)

    for string in messages:
        await bot_msg.edit(content=string)
        print(f'已分析完畢 {msg.author.name} 的圖片。')

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

def save_data(data: dict,data_file: str):
    '''
    儲存檔案
    '''
    with open(f'{data_file}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# ==================================================

log: dict[int, list[str]] = {} # 創建一個名稱叫 log 的字典, 用來存放短期記憶
config_data: dict = json.load(open('config.json', encoding='utf-8')) # 讀取 config 的資料

mode = config_data.get('mode', '')

while True:
    if mode in ['whitelist', 'blacklist']: break

    mode = input('不明的模式，模式應為 "whitelist" 或 "blacklist"\n輸入執行模式: ')

config_data['mode'] = mode
save_data(config_data, "config")

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config_data['prefix']), intents=discord.Intents.all()) # 設定 Discord bot

status = cycle(['Gemini chat bot', '我是 AI 機器人', '正在聊天']) #機器人顯示的個人狀態,可自行更改

@tasks.loop(seconds=10) # 每隔 10 秒更換一次機器人個人狀態
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_ready():
    print(f'{bot.user} 已上線，正在執行 {"白名單" if mode == "whitelist" else "黑名單"} 模式！')
    change_status.start() # 讓機器人顯示狀態

if mode == 'whitelist':
    @bot.command()
    @commands.guild_only()
    async def openchannel(ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        '''
        新增白名單內頻道
        '''
        channel = channel or ctx.channel

        channel_id, channel_list, data= load_channel_data(channel)

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

elif mode == "blacklist":
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
        await ctx.reply(f'{channel.mention} 的短期記憶已清空。', mention_author=False)
    else:
        await ctx.reply('並無儲存的短期記憶。', mention_author=False)

@bot.listen('on_message')
async def when_someone_send_somgthing(msg: discord.Message): # 如果有訊息發送就會觸發
    command_name = msg.content.removeprefix(config_data['prefix'])
    if (command_name in [cmd.name for cmd in bot.commands]) or msg.author.bot: return

    can_send = msg.channel.permissions_for(msg.guild.me).send_messages # can_send 用來檢查頻道是否有發言權限
    if not can_send: # 如果機器人沒有發言權限
        print(f'沒有權限在此頻道 ({msg.channel.name}) 發言。')
        return # 不再執行下方程式

    result = load_channel_data(msg.channel)
    channel_id, channel_list = result[0], result[1]

    if (mode == 'whitelist' and channel_id not in channel_list) or (mode == 'blacklist' and channel_id in channel_list): return # 判斷頻道 id 是否在 channel_list 裡面

    if msg.attachments: # 如果訊息中有檔案
        for attachment in msg.attachments: # 遍歷訊息中檔案
            if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']): # 檢測副檔名
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp: # 讀取圖片的 url 並將他用 aiohttp 函式庫轉換成數據
                        if resp.status != 200:
                            await msg.reply('圖片載入失敗。', mention_author=False) # 如果圖片分析失敗就不再執行下方程式
                            return

                        print(f'正在分析 {msg.author.name} 的圖片...')
                        bot_msg = await msg.reply('正在分析圖片...', mention_author=False)
                        image_data = await resp.read() # 定義 image_data 為 aiohttp 回應的數據
                        dc_msg = format_discord_message(msg.content) # 格式化訊息
                        response_text = await image_api(image_data, dc_msg) # 用 image_api 函式來發送圖片數據跟文字給 api
                        await split_and_edit_message(msg, bot_msg, response_text, 1700) # 如果回應文字太長就拆成兩段
                        await update_message_history(msg.channel.id,f"{msg.author.name}傳送了一張圖片，內容是'{response_text}'")
                        return

        # 通過爬蟲來獲取網址網站標題, 進行簡單的連結判讀
        links = islink(msg.content)
        if links: # 如果訊息內容有連結
            title = gettitle('\n'.join(links)) # 取得連結中的 title
            word = msg.content.replace(links, f'(一個網址, 網址標題是: "{title}")' if title else '(一個網址, 網址無法辨識)')
            await update_message_history(msg.channel.id, f'「{msg.author.name}」 : "{word}"')
            reply_text = await text_api(prompt + get_message_history(msg.channel.id))
            await msg.reply(reply_text, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            print(msg.author.name + ":" + msg.content + "\n" + reply_text)
            return

    # 就是 print 出來訊息的詳細資料, 可以不用加
    # ==========================================
    print(f'Server name: {msg.guild.name if not isinstance(msg.channel, discord.DMChannel) else "私訊"}')
    print(f'Message ID: {msg.id}')
    print(f'Message Content: {msg.content}')
    print(f'Author ID: {msg.author.id}')
    print(f'Author Name: {msg.author.name}')
    if not isinstance(msg.channel, discord.DMChannel):
        print(f'Channel name: {msg.channel.name}')
        print(f'Channel id: {msg.channel.id}')
    # ==========================================

    dc_msg = format_discord_message(msg.content) # 將訊息內容放入 format_discord_message, 簡單來說就是更改訊息的格式, 然後把回傳結果放入 dc_msg 變數
    update_message_history(msg.channel.id, f'{msg.author.name}: ' + dc_msg) # 將 dc_msg (就是使用者發送的訊息) 上傳到短期記憶
    reply_text = await text_api(prompt + (get_message_history(msg.channel.id) if (msg.channel.id) in log else msg.content))

    await msg.reply(reply_text, mention_author=False, allowed_mentions=discord.AllowedMentions.none()) # 將回應回傳給使用者
    update_message_history(msg.channel.id, f'你回應{msg.author.name}:' + reply_text) # 將 api 的回應上傳到短期記憶

bot.run(config_data['token'])