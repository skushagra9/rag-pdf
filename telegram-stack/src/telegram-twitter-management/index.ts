
import TelegramBot, { Message } from 'node-telegram-bot-api';
import { TwitterApi, TweetV2PostTweetResult } from 'twitter-api-v2';
import {  TELEGRAM_BOT_TOKEN_TELEGRAM_TWITTER_MANAGEMENT, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_API_KEY, TWITTER_API_SECRET_KEY } from '../utils';
import { generateTweetDraft } from './generateTweet';

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN_TELEGRAM_TWITTER_MANAGEMENT, { polling: true });

const twitterClient = new TwitterApi({
  appKey: TWITTER_API_KEY,
  appSecret: TWITTER_API_SECRET_KEY,
  accessToken: TWITTER_ACCESS_TOKEN,
  accessSecret: TWITTER_ACCESS_TOKEN_SECRET,
});

type PendingTweet = { id: number; text: string };
const pendingTweets: Record<number, PendingTweet[]> = {};

//initialize text
bot.onText(/\/start/, (msg: Message) => {
  bot.sendMessage(msg.chat.id, 'Hello! Use /tweet <idea> to begin drafting a tweet.');
});

// /tweet <idea>
bot.onText(/\/tweet (.+)/, async (msg: Message, match: RegExpExecArray | null) => {
  if (!msg.chat || !match) return;
  const chatId = msg.chat.id;

  const idea = match[1]?.trim();
  if (!idea) {
    await bot.sendMessage(chatId, 'Usage: /tweet <idea>');
    return;
  }

  const draft = await generateTweetDraft(idea);

  if (!pendingTweets[chatId]) pendingTweets[chatId] = [];

  const tweetId = Date.now();
  pendingTweets[chatId].push({ id: tweetId, text: draft });
  await bot.sendMessage(
    chatId,
    `**Proposed Tweet Draft:**\n\n${draft}\n\nUse /list to list all the tweets.`,
    { parse_mode: 'Markdown' }
  );
});

//list all the pending orders
bot.onText(/\/list/, async (msg: Message) => {
  if (!msg.chat) return;
  const chatId = msg.chat.id;
  const tweets = pendingTweets[chatId] || [];

  if (tweets.length === 0) {
    bot.sendMessage(chatId, 'No pending tweets. Use /tweet <idea> first.');
    return;
  }

  // Generate inline keyboard options
  const keyboard = {
    inline_keyboard: tweets.map((tweet) => [
      {
        text: tweet.text.substring(0, 90) + "...", // Show first 90 chars as button text
        callback_data: `tweet_${tweet.id}`, // Unique identifier for the tweet
      },
    ]),
  };

  bot.sendMessage(chatId, '📝 **Select a Tweet to Manage:**', {
    parse_mode: 'Markdown',
    reply_markup: keyboard,
  });
});

//after clicking on approve
bot.on('callback_query', async (query) => {
  if (!query.message || !query.data) return;
  const chatId = query.message.chat.id;
  const messageId = query.message.message_id;

  if (query.data.startsWith('approve_')) {
    const tweetId = parseInt(query.data.replace('approve_', ''));
    const tweetIndex = (pendingTweets[chatId] || []).findIndex((t) => t.id === tweetId);

    if (tweetIndex === -1) {
      bot.answerCallbackQuery(query.id, { text: 'Tweet not found.' });
      return;
    }

    const tweet = pendingTweets[chatId][tweetIndex];

    try {
      const res = await twitterClient.v2.tweet(tweet.text);
      const tweetUrl = `https://twitter.com/i/web/status/${res.data.id}`;

      // Remove the approved tweet from the pending list
      pendingTweets[chatId].splice(tweetIndex, 1);

      bot.editMessageText(`✅ Tweet posted successfully!\n🔗 [View Tweet](${tweetUrl})`, {
        chat_id: chatId,
        message_id: messageId,
        parse_mode: 'Markdown',
      });
    } catch (error) {
      console.error('Twitter Post Error:', error);
      bot.sendMessage(chatId, '❌ Failed to post tweet.');
    }
  }
});

//after clicking a tweet from /list
bot.on('callback_query', async (query) => {
  if (!query.message || !query.data) return;
  const chatId = query.message.chat.id;
  const messageId = query.message.message_id;
  const tweetId = parseInt(query.data.replace('tweet_', ''));

  const tweet = (pendingTweets[chatId] || []).find((t) => t.id === tweetId);
  if (!tweet) {
    bot.answerCallbackQuery(query.id, { text: 'Tweet not found.' });
    return;
  }

  // Inline keyboard with Approve and Edit options
  const keyboard = {
    inline_keyboard: [
      [{ text: '✅ Approve & Post', callback_data: `approve_${tweet.id}` }],
      [{ text: '✏️ Edit', callback_data: `edit_${tweet.id}` }],
    ],
  };

  bot.editMessageText(
    `📝 **Selected Tweet:**\n\n${tweet.text}\n\nChoose an action:`,
    {
      chat_id: chatId,
      message_id: messageId,
      parse_mode: 'Markdown',
      reply_markup: keyboard,
    }
  );
});

//click on edit 
bot.on('callback_query', async (query) => {
  if (!query.message || !query.data) return;
  const chatId = query.message.chat.id;
  const messageId = query.message.message_id;

  if (query.data.startsWith('edit_')) {
    const tweetId = parseInt(query.data.replace('edit_', ''));
    const tweet = (pendingTweets[chatId] || []).find((t) => t.id === tweetId);

    if (!tweet) {
      bot.answerCallbackQuery(query.id, { text: 'Tweet not found.' });
      return;
    }

    bot.sendMessage(chatId, `✏️ Send the new text for tweet ID *${tweetId}*:`, { parse_mode: 'Markdown' });

    // Listen for next message to edit the tweet
    bot.once('message', (msg) => {
      if (!msg.text) return;
      tweet.text = msg.text;

      bot.sendMessage(chatId, `✅ Tweet updated:\n🆔 ${tweetId}\nNew Text: ${msg.text}`);
    });
  }
});
