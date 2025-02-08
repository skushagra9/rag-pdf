import TelegramBot from 'node-telegram-bot-api';
import { API_URL, TELEGRAM_BOT_TOKEN_TELEGRAM_RAG } from '../utils';

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN_TELEGRAM_RAG, { polling: true });

// Basic message handler
bot.onText(/.*/, async (msg) => {
  const chatId = msg.chat.id;
  const userQuery = msg.text;

  console.log("User Query: ", userQuery);

  // Make API call to your server for RAG response
  try {
    const response = await fetch(`${API_URL}/search/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userQuery })
    });
    const data = await response.json();

    if (data.answer) {
      bot.sendMessage(chatId, data.answer);
    } else {
      bot.sendMessage(chatId, "I don't know the answer.");
    }
  } catch (error) {
    bot.sendMessage(chatId, "Error while fetching data.");
    console.error("Error:", error);
  }
});
