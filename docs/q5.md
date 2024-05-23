## No such file or directory: 'config.json/channel.json'

如果你出現以上錯誤表示找不到你的檔案，請檢查你的檔案是否在正確路徑上。

如果確定檔案存在，請確認檔案路徑上沒有兩個相同名稱的資料夾。

例如: 'C:\Downloads\bot\bot\main.py'

這種路徑就容易會發生錯誤，請嘗試將機器人資料夾換個位置。

如果還是沒有解決，請嘗試以下方法：

把
```py
#只要有這段的地方都需要改
data = json.load(open('config.json', encoding='utf-8'))
```
改成
```py
# 要先import os
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, 'config.json')
data = json.load(open(config_path, encoding='utf-8'))
```
channel.json 也是同理
```py
#只要有這段的地方都需要改
with open('channel.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```
改成
```py
#要先import os
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, 'channel.json')
with open(config_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```
這樣應該就能解決問題了，其他問題可以到 Issues 或 Discord 私訊 `yimang__` 或 `bruh0422`