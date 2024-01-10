# 介紹
這是一個利用google開發的gemini模型的api來連接discord機器人的Chat bot
## 指令
**以下所有指令都不需要任何prefix或mention**
* blockchannel ➡️ 不再接收當前頻道的訊息(封鎖頻道)
* unblockchannel ➡️ 解除當前頻道的封鎖
* reset ➡️ 清除該用戶的短期記憶
## 注意事項
*私訊(dm channel)和伺服器頻道的使用方法是一模一樣的*

*這個版本是每則訊息都會回覆, 不需要mention。所以一次太多訊息他會卡住*

*回覆時機器人和真人用戶都會回覆,並且reply會有mention,所以如果你有其他機器人建議用私訊(dm)使用,不然機器人們可能會吵起來*

*blockchannel和unblockchannel指令需要等他處理完前面堆積的api請求才會執行*

*每個用戶的短期記憶是分開的,reset只會清空當前使用指令的用戶的短期記憶*

*短期記憶的上限包含機器人的回覆*


# 常見問題
### 如何取得gemini api key
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

### 如何產生訓練prompt
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

![圖11](https://media.discordapp.net/attachments/1141922914178977946/1194681305082900480/image.png?ex=65b13cab&is=659ec7ab&hm=b17ce7b59c3ab113e0a8d399a347bbc2d208bcc5bf9eb3fac4dc3518584e210d&=&format=webp&quality=lossless&width=722&height=662)

把框起來的那段換成自己的prompt就可以囉

![圖12](https://media.discordapp.net/attachments/1141922914178977946/1194681593520984184/image.png?ex=65b13cf0&is=659ec7f0&hm=7adb953e49323047878352ebd19c206eeab0181272cbbd524c0e68334bd28eb6&=&format=webp&quality=lossless&width=722&height=662)

