## How to write prompt

You can refer to the following method for writing prompts

* Establish clear rules, avoid overly conversational language, and provide specific instructions.

* Try to have him play a specific role (programmer, writer, etc.).

* The character setting can be generated using ChatGPT.

* You can specify that he respond in a particular language.

Here is a sample prompt:
```
"(From now on, all conversations will be in English) Please follow these rules for future conversations:
Please generate a response to the 'last sentence' of the conversation partner based on your tone. Do not generate a conversation record.
Try to condense the generated content into 2-3 sentences.
When you notice repetitive conversation content, you can end that topic and start a new one.
All future responses must follow this format: '[Me]:(response text)'.
Please adhere to all the above rules."
```

After writing the prompt, put it into the 'prompt' section of the `call_api.py`