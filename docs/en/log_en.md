- 2024/5/23
    - Merge main_whitelist.py into main.py
    - Optimize the formatting
    - Change the commands to prefixed commands

- 2024/6/8
    - Streamline the code to allow the reset command to be used in DM channels

- 2024/6/14
    - Modified the file and function names to make them more intuitive to use

- 2024/6/19
    - The issues regarding the inability to detect command messages and inability to use have been fixed
    - Integrating image recognition results into short-term memory

- 2024/6/20
    - Modified the structure of the prompt, splitting it into two parts: 'history' and 'prompt'

- 2024/7/28
    - Because Google AI no longer supports Gemini Pro Vision, the image recognition model has been changed to Gemini 1.5 Flash

- 2024/8/5
    - Fixed the issue where the whitelist mode could not be used in DM channels

- 2024/10/13
    - Fixed an issue where messages containing multiple URLs could not be processed by the web scraper

- 2025/02/16
    - Fix the issue where the web scraper is not working and add a Dockerfile

- 2025/03/15
    - Since the Google Gemini API no longer supports the gemini-1.0-pro model, the image recognition model has been switched to gemini-1.5-pro

- 2025/03/26
    - Change image response structure