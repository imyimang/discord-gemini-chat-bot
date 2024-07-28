## Choosing between different models in Gemini
Gemini released free versions 1.0 and 1.5, both of which are free to use. The relevant rate limits are as shown in the image below.
![圖13](../images/11.png)

If you're using the free version, it's recommended to use 1.0. Although 1.5 has optimized models, its rate limits are quite strict.

To change the model, simply go to `call_api.py`
```py
...

model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config=generation_config, safety_settings=safety_settings) 

image_model = genai.GenerativeModel(model_name='gemini-pro-vision', generation_config=generation_config, safety_settings=safety_settings)

...
```
This part

Change
```py
model_name='gemini-1.0-pro'
```
to
```py
model_name='gemini-1.5-pro'
```
You can make changes according to the model you want.
> [!WARNING]  
> Starting from July 12, 2024, Google AI will no longer support Gemini 1.0 Pro Vision api. Please use Gemini 1.5 Flash or other models.