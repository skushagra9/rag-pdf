
# Telegram Twitter Bots

**Installation Steps:**
```sh
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  

# Pull the Llama model
ollama pull llama3.2:1b

# Run the model
ollama run llama3.2:1b
```

```sh
git clone https://github.com/skushagra9/rag-pdf
cd telegram-stack
npm install 
cp .env.example .env
```

Fill in the env variables

```sh 
npm run rag-tg
```
[TG-RAG Bot Readme (Demo Video Too)](https://github.com/skushagra9/rag-pdf/blob/master/telegram-stack/src/rag-telegram/Readme.md)

it would start running the telegram bot


```sh 
npm run content-advisor
```
[Content-Advisor Bot Readme (Demo Video too)](https://github.com/skushagra9/rag-pdf/blob/master/telegram-stack/src/telegram-twitter-management/Readme.md)

it would start running the content-advisor bot
