import * as dotenv from 'dotenv';
dotenv.config();

export const TELEGRAM_BOT_TOKEN_TELEGRAM_TWITTER_MANAGEMENT = process.env.TELEGRAM_BOT_TOKEN_TELEGRAM_TWITTER_MANAGEMENT || '';
export const API_URL = process.env.API_URL || '';
export const TELEGRAM_BOT_TOKEN_TELEGRAM_RAG = process.env.TELEGRAM_BOT_TOKEN_TELEGRAM_RAG || '';
export const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';
export const TWITTER_API_KEY = process.env.TWITTER_API_KEY || '';
export const TWITTER_API_SECRET_KEY = process.env.TWITTER_API_SECRET_KEY || '';
export const TWITTER_ACCESS_TOKEN = process.env.TWITTER_ACCESS_TOKEN || '';
export const TWITTER_ACCESS_TOKEN_SECRET = process.env.TWITTER_ACCESS_TOKEN_SECRET || '';
