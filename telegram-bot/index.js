import TelegramBot from 'node-telegram-bot-api';
import dotenv from 'dotenv';

dotenv.config();
const token = process.env.TELEGRAM_BOT_TOKEN;

const bot = new TelegramBot(token, { polling: true });

// Basic message handler
bot.onText(/.*/, async (msg) => {
  const chatId = msg.chat.id;
  const userQuery = msg.text;

  console.log("User Query: ", userQuery);

  // Make API call to your server for RAG response
  try {
    const response = await fetch('https://98bb-2405-201-400b-90b8-c4dd-ea75-13cb-3c33.ngrok-free.app/query', {
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
