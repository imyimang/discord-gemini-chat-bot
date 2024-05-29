The bot's memory is stored in the form of Python dictionaries in memory, while channel.json is responsible for storing channel blacklists/whitelists.

## Memory principle
```py
{'channel_id1': 'value1', 'channel_id2': 'value2', 'channel_id3': 'value3'}
```
When a user sends a message, the message is stored in a dictionary with the channel ID corresponding to the value, and then the value is sent to the API, thus achieving the ability of short-term memory.

**It's not long-term memory; the data in memory will disappear once the system restarts.**

## Flowchart
![alt text](../images/12.jpg)
