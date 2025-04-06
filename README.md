# ChatyBot

An interactive, adaptive and personalized AI chatbot built with Ollama and LangChain

---

## Features

- Personality-driven replies
- Remembers key moments with TinyDB memory
- Keeps chat context and summarizes it every 5 messages
- Uses local LLMs via [Ollama](https://ollama.com)

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed
- A model pulled and running (e.g. `mistral`)

---

## Getting Started

1. Clone the repo:
```bash
git clone https://github.com/LucasOrsatti/Chatybot.git
cd ChatyBot
pip install -r requirements.txt
python chatbot.py
```
You might need to create a virtual enviroment if you wish to keep the libraries local and not global.

---

## What should I know?
By default, the memory will be saved in the memory.json file, which will be created if one does not already exist. This file can be changed and edited, but keep in mind that this may change the performance of the bot.

The bot's personality is written in the chatybot.py file. You can change it to make the bot exactly the way you want it. When writing the bot's personality, try to keep it as concise as possible. AI processing requires a lot of processing power, so the less we demand, the faster the response will be.

---

## Disclaimer!
This is an AI, nothing it says should be taken seriously! We are using Mistral, an uncensored model, so the bot's output may not be safe for all ages or audiences. Try to keep chats within legal limits. I am not responsible for the bot's response or user input!

---

## Thanks!
Thank you for looking at my GitHub page! I hope you enjoyed my work and have some fun with this simple script. Feel free to leave you feedback on the comments.
