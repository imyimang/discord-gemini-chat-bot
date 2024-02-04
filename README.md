# 介紹
這是一個利用google開發的gemini模型的api來連接discord機器人的Chat bot

* 頻道具有黑白名單兩種模式(請見**常見問題**)

* 文字聊天具有短期記憶功能(記憶句數上限可自訂)

* 能夠進行圖片辨識

* 能在DM channel中使用

## 指令(預設為黑名單模式)
**以下所有指令都不需要任何prefix或mention**

*注意:以下指令都沒有設定任何權限限制,任何人都能使用*

* blockchannel ➡️ 不再接收當前頻道的訊息(封鎖頻道)
* unblockchannel ➡️ 解除當前頻道的封鎖
* blockserver ➡️ 不再接收當前伺服器**所有頻道**的訊息
* reset ➡️ 清除該用戶的短期記憶
## 注意事項
*私訊(dm channel)和伺服器頻道的使用方法是一模一樣的*

*這個版本是***每則訊息都會回覆**, **不需要mention**。*所以一次太多訊息他會卡住*

*回覆時機器人和真人用戶都會回覆,所以如果你有其他機器人建議用私訊(dm)使用,不然機器人們可能會吵起來*

*blockchannel和unblockchannel指令需要等他處理完前面堆積的api請求才會執行*

**每個用戶的短期記憶是分開的**,*reset只會清空當前使用指令的用戶的短期記憶*

*短期記憶的上限包含機器人的回覆*

*短期記憶僅包含文字回應,不包含圖片回應*
## 前置作業
將需要的機器人設定填入config.json中

這樣就完成前置作業了
# 常見問題
## 我想要把channel.json改成頻道白名單而不是黑名單怎麼辦
如果想要讓機器人只會回覆channel.json裡面的頻道的訊息,而不是封鎖裡面的頻道

請使用專案中的**main_whitelist.py**

Def.py無須更改

**白名單版本的指令如下:**

*注意:以下指令都沒有設定任何權限限制,任何人都能使用*
* openchannel ➡️ 將當前頻道加入白名單
* closechannel ➡️ 將當前頻道移出白名單
* reset和原版相同




## 如何取得gemini api key
1.前往gemini的網站 [**點我**](<https://makersuite.google.com/>)

2.登入你的google帳號(要帳戶年滿18歲) [**詳情點我**](<https://ai.google.dev/available_regions?hl=zh-tw>)

3.打勾同意用戶條款然後按繼續
![圖1](https://media.discordapp.net/attachments/1128696283276783688/1194674355217641512/image.png?ex=65b13632&is=659ec132&hm=4a068bf88e4cac46219dfbc4c80596a784c0e9f2a1bae6f58f09f836dd5f43b2&=&format=webp&quality=lossless&width=1081&height=570)

4.點get api key
![圖2](https://media.discordapp.net/attachments/1128696283276783688/1194675382012624986/image.png?ex=65b13727&is=659ec227&hm=e5a35f34c4dc5b2f558222977076d3d075539895c02219db7f53d77c4d1ac816&=&format=webp&quality=lossless&width=1081&height=562)

5.點create api key
![圖3](https://media.discordapp.net/attachments/1128696283276783688/1194675688846930070/image.png?ex=65b13770&is=659ec270&hm=bba87747b250fa3a6c5774807866428af5721e3fc63f65ceea485a80b24a457b&=&format=webp&quality=lossless&width=1081&height=571)

6.這樣就得到api key囉 點copy就能複製
![圖4](https://media.discordapp.net/attachments/1128696283276783688/1194676224111431831/image.png?ex=65b137ef&is=659ec2ef&hm=8cc21d0ecdf0d428d8d15d052e8494c1597808ecda401848db788ed4c1ba461a&=&format=webp&quality=lossless&width=1081&height=570)


## 如何產生訓練prompt
1.前往gemini的網站 [**點我**](<https://makersuite.google.com/>)

2.點create new,然後選Chat prompt
![圖5](https://media.discordapp.net/attachments/1141922914178977946/1194679445739552818/image.png?ex=65b13aef&is=659ec5ef&hm=04155b8a51654cd61d85d3bcef075bfb3766c64a0d9d1ba61ad9226adb73f765&=&format=webp&quality=lossless&width=1081&height=505)

3.先隨便打點東西然後按Save
![圖6](https://media.discordapp.net/attachments/1141922914178977946/1194679702577758300/image.png?ex=65b13b2d&is=659ec62d&hm=3ed1ae144bdc72472eed173b5d9452f28b640a93f86f3dbdf562bd59e4f0049d&=&format=webp&quality=lossless&width=1081&height=507)
名字不取也沒關係可以直接按Save

4.接下來就能開始訓練啦
![圖7](https://media.discordapp.net/attachments/1141922914178977946/1194680165784096858/image.png?ex=65b13b9b&is=659ec69b&hm=c00c283623122dcae087f1439166c9a24fc54e5ada7e489a6114295c679db89d&=&format=webp&quality=lossless&width=1081&height=507)

* User的地方就是你要問的問題
* Model的地方就是你想要他怎麼回答
也可以直接用對話紀錄然後把你想要模擬的對象放在Model的地方,自己放在User的地方

5.匯出你的prompt
點擊右上角的Get code就能匯出啦
![圖8](https://media.discordapp.net/attachments/1141922914178977946/1194680597700935871/image.png?ex=65b13c02&is=659ec702&hm=e64e5f6a8ac662ec198b5c3c527b884113cee0bf7b8b58d7a8e4242ef133ab00&=&format=webp&quality=lossless&width=1081&height=507)
選Python 然後往下滑一點
![圖9](https://media.discordapp.net/attachments/1141922914178977946/1194680841733935204/image.png?ex=65b13c3c&is=659ec73c&hm=afe977493e77b2c8ada07a176fb9d08e1357251e83eaa99985281b546ff05d68&=&format=webp&quality=lossless&width=1058&height=662)
這段就是你的prompt了
![圖10](https://media.discordapp.net/attachments/1141922914178977946/1194681056675246212/image.png?ex=65b13c70&is=659ec770&hm=2c1790bc3ffd202fc163006dd9edb8a19c254ed42c0b4fccddfefd65aa976a0f&=&format=webp&quality=lossless&width=1073&height=662)

6.回到Def.py

![圖11](https://media.discordapp.net/attachments/1141922914178977946/1194693909532659813/image.png?ex=65b14868&is=659ed368&hm=002956110a0db9196c47fc5a113100235015ead332e76e3a0cf8831a0fd33a86&=&format=webp&quality=lossless&width=1088&height=662)

把框起來的那段換成自己的prompt就可以囉

![圖12](https://media.discordapp.net/attachments/1141922914178977946/1194694334709239858/image.png?ex=65b148cd&is=659ed3cd&hm=f7d67816f2cf8ac10e07f255a52c325499b77b8d631c81084b48286ff2c71517&=&format=webp&quality=lossless&width=1140&height=662)


## The caller does not have permisson
當你點擊創建api key的時候,可能會出現下面的錯誤
![圖13](https://media.discordapp.net/attachments/1141922914178977946/1194873264883892274/image.png?ex=65b1ef72&is=659f7a72&hm=92f15571007a5cde99e807d45ddbd118fb05762539e0f4f0fad04bfefbaff9aa&=&format=webp&quality=lossless&width=1017&height=662)
這可能是由於你刪除了你的前一個api key

這種情況建議用另一個沒創過api key的帳號

重新創建一個api key

## Reset指令無效
抱歉,我們的錯,我們的程式出現了bug

請下載最新版的code,我們已經解決了