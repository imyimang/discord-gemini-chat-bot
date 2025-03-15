## Commands (defaulting to blacklist mode)

*Note: The following commands have no permission restrictions and can be used by anyone.*

- Whitelist mode(Default)
    - openchannel ➡️ add channel to whitelist
    - closechannel ➡️ remove channel from whitelist
- Blacklist mode
    - blockchannel ➡️ add channel to blacklist
    - unblockchannel ➡️ remove channel from blacklist
- reset ➡️ Clearing short-term memory in the channel

## Points to note
- All commands above are prefixed commands.
- Command can't be used in DM channel(Except for the reset command)
- This bot will reply **every message**,**don't need mention (@)**,so if you sent message too quick,it might get stuck.
- In whitelist mode, only the reset command can be used in DM channels; opening or closing channels is not allowed.
- **Short-term memory for each channel is separate**, the reset command only clears the short-term memory of the specified channel.
- The maximum sentence limit of short-term memory includes responses from the bot.
- If the mode specified in config.json is not "blacklist" or "whitelist", it will cause the bot to be unable to use commands.
