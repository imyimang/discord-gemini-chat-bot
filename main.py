
import re
from datetime import datetime,timezone,timedelta
import discord
import google.generativeai as genai
from discord.ext import commands
import asyncio
import random
import json
from Def import history #從Def.py導入history副函式(主要是我不想要檔案太長,你想要把函式放到這個檔案也可以)

#如果你想要看懂整個程式
#建議去科普一下json檔,python字典,python副函式的運作原理


log = {} #創建一個名稱叫log的字典 用來存放短期記憶

bot = commands.Bot(command_prefix="*", intents=discord.Intents.all()) #設定discord bot,prefix可以自己改


@bot.event
async def on_message(msg):   #如果有訊息發送就會觸發
   
    if msg.author == bot.user:   #如果訊息發送者是自己就不再執行下面的程式
        return
    if isinstance(msg.channel, discord.TextChannel):   #如果訊息在文字頻道就執行下面
      can_send = msg.channel.permissions_for(msg.guild.me).send_messages   #can_send用來檢查頻道是否有發言權限
      if bool(can_send) != True:   #如果機器人沒有發言權限就不執行下面程式
          print("沒有權限在此頻道發言")
          return
    
    if msg.content == "unblockchannel":   #如果訊息內容="unblockchannel"就執行下面
        channel_id = str(msg.channel.id)   #定義channel_id為發送訊息的頻道id
        with open('channel.json', 'r', encoding='utf-8') as file:   #打開json檔案
        
        #此處的json檔就是黑名單列表的概念

            data = json.load(file)   #定義data為json檔案裡面讀到的資料
        channel_list = data.get("id", [])   #定義channel_list為json裡面鍵值為"id"的資料,如果沒有這個資料就返回空的列表
        
        if str(msg.channel.id) in channel_list: #如果channel id在channel_list裡面(因為這個json檔只有存一個鍵值,所以基本上就是在json檔裡面的意思)
            channel_list.remove(channel_id)   #從json檔裡面移除channel_id(就是頻道id)這個資料
            await msg.reply("頻道已解除屏蔽")

        data["id"] = channel_list
        with open('channel.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)   #儲存上面json檔變更的內容
        return 

    if msg.content == "blockchannel":  #如果訊息內容="blockchannel"就執行下面
       channel_id = str(msg.channel.id)  #定義channel_id變數為頻道id
       with open('channel.json', 'r', encoding='utf-8') as file:
            data = json.load(file)  #打開json檔
       channel_list = data.get("id", [])  #取得json檔裡面的資料
       if str(msg.channel.id) in channel_list: #如果頻道id已經記錄在json檔案裡面的話就執行下面
           await msg.reply("該頻道已被屏蔽")
           return
       channel_list.append(channel_id)  #如果json裡面沒有此頻道id,就把此頻道id加入json檔
       data["id"] = channel_list
       with open('channel.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)  #儲存變更
       await msg.reply("頻道已成功屏蔽")
       return
    
    channel_id = str(msg.channel.id) #定義變數channel_id
    with open('channel.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  #開啟json檔
    channel_list = data.get("id", [])
    if channel_id in channel_list:  #如果頻道id在json檔裡面
        return #就不執行下面程式
    
    t = random.randint(0, 2)  #讓機器人隨機停頓0~2秒後再之行下面(這兩行可以不用)
    await asyncio.sleep(t)


    # 就是print出來訊息的詳細資料 可以不用加
    #==========================================
    if isinstance(msg.channel, discord.TextChannel):
      print(f"Server name:{msg.guild.name}")
    print(f"Message ID: {msg.id}\t(私訊)")
    print(f"Message Content: {msg.content}")
    print(f"Author ID: {msg.author.id}")
    print(f"Author Name: {msg.author.name}")
    if isinstance(msg.channel, discord.TextChannel):
      print(f"Channel name: {msg.channel.name}")
      print(f"Channel id: {msg.channel.id}")
    #==========================================
    
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc) 
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  #定義一個時間變數(寫message log用的,如果沒有要用message log可以不用這兩行)

    reply_text = await history(get_formatted_message_history(msg.author.id)) #將訊息發送者的id放入get_formatted_message_history函式(後面會講),然後將得到的歷史資料放入history函式來得到api回應

    await msg.reply(reply_text)  #將api的回應回傳給使用者

    dc_msg = clean_discord_message(msg.content) #將訊息內容放入clean_discord_message(下面會講),簡單來說就是更改訊息的格式,然後把回傳結果放入dc_msg變數
    update_message_history(msg.author.id, dc_msg) #將dc_msg(就是使用者發送的訊息)上傳到短期記憶
    update_message_history(msg.author.id, reply_text) #將api的回應上傳到短期記憶


#下面是message log,沒有需要可以不用加
    #==========================================
    f = open('ai_log.txt', "a", encoding="utf-8")
    mt = dt2.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(msg.channel, discord.TextChannel):
      f.write(f"===============\n{mt}\n\n{msg.author.name}({msg.author.id})\t在\t{msg.guild.name}({msg.guild.id})\t傳送:\n{msg.content}\n")
    else:
      f.write(f"===============\n{mt}\n\n{msg.author.name}({msg.author.id})\t在\t私訊\t傳送:\n{msg.content}\n")
        
  
    f.write(f"\nAI回應:\n{reply_text}\n")
    #==========================================
      

      
def update_message_history(user_id, text): #定義update_message_history副函式
    if user_id in log:  #如果user_id在字典裡面
        log[user_id].append(text)   #就把text加入以user_id命名的鍵中
        if len(log[user_id]) > 15: #如果user_id裡面存的資料大於15筆(數字可以自己設定,不一定要15,這代表了他的短期記憶容量)
            log[user_id].pop(0) #就pop最早的一筆資料
    else:
        log[user_id] = [text] #如果user_id不在字典裡就創建一個,並把text放入

def clean_discord_message(input_string): #刪除 Discord 聊天訊息中位於 < 和 > 之間的文字(讓他能夠放入短期記憶並被ai讀懂)
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content
    
def get_formatted_message_history(user_id):
    if user_id in log: #如果user_id有在log字典裏面
        return '\n\n'.join(log[user_id]) #返回user_id裡面存放的內容
    else:
        return  #如果user_id不在字典裡就返回

    
bot.run("your token")   #放入你的discord bot token