## How to generate prompts for training
1. Visit the Gemini website. [**click me**](<https://makersuite.google.com/>)

2. Click "Create new"，then choose "Chat prompt"
![圖5](../images/5.png)

3.Write something and click "Save"
![圖6](../images/6.png)
You can directly click "Save" without naming if you prefer.

4.Export your prompt.
Click "Get code" to export
![圖7](../images/7.png)

Choose "Python" 

This segment is your prompt.
![圖9](../images/8.png)

5.Go back to call_api.py

![圖11](../images/9.png)

You just need to replace the highlighted segment with your own prompt.

![圖12](../images/10.png)

* "User" is the question you want to ask
* "Model" is where you specify how you want it to respond

You can also directly use conversation transcripts and place the entity you want to simulate under "Model" and yourself under "User".

Simply copy the format of the prompt and change the content inside.