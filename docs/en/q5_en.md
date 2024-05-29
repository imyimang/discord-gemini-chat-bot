## No such file or directory: 'config.json/channel.json'

If you encounter the above error, it means the file cannot be found. Please check if the file exists in the correct path.

If you're sure the file exists, make sure there are no two folders with the same name along the file path.

For example: 'C:\Downloads\bot\bot\main.py'

This kind of path can lead to errors. Try moving the bot folder to a different location.

If the issue persists, please try the following methods:

Change
```py
data = json.load(open('config.json', encoding='utf-8'))
```
to
```py
# need to import os first
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, 'config.json')
data = json.load(open(config_path, encoding='utf-8'))
```
The same applies to channel.json
```py
with open('channel.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```
to
```py
#need to import os first
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, 'channel.json')
with open(config_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```
This should solve the problem. For other issues, you can go to Issues or send a private message to `yimang__` or `bruh0422`