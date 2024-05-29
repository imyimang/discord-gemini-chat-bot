## 我想要把 channel.json 改成頻道白名單而不是黑名單怎麼辦?

如果想要讓機器人只會回覆 channel.json 裡面的頻道的訊息，而不是封鎖裡面的頻道，請更改 config.json 中的 **'mode'**。

Def.py 無須更改。

**白名單版本的指令如下:**

*注意: 以下指令都沒有設定任何權限限制，任何人都能使用。*
- openchannel ➡️ 新增白名單內頻道
- closechannel ➡️ 移除白名單內頻道
- reset 和原版相同