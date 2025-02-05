import OpenAI from "openai";
import { OPENAI_API_KEY } from "../utils";

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY
})


export async function generateTweetDraft(idea: string): Promise<string> {
  try {
    // Using ChatCompletion with GPT-3.5-turbo, but you can switch models or prompt style
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: `
            You are an expert social media strategist with a deep understanding of Twitter engagement tactics. 
            Your task is to craft highly engaging, viral-ready tweets that spark discussions, get retweets, and encourage interaction.
    
            **Guidelines:**
            - The tweet **must fit within 280 characters**.
            - Use a **conversational, witty, or thought-provoking tone** depending on the topic.
            - **Maximize engagement** by making it catchy, relatable, or controversial (but not offensive).
            - Use relevant **hashtags** to reach a broader audience.
            - If applicable, mention important **Twitter handles (@usernames)** or trending topics.
            - If humor is relevant, **inject a bit of wit** or a **bold statement** to grab attention.
            - Avoid filler words—**every character should add value**.
            - If the topic is news-related, **make it urgent and attention-grabbing**.
            - **No forced AI-like phrasing**—make it feel **authentic** and **human-written**.
          `,
        },
        {
          role: 'user',
          content: `
            Create a viral and highly engaging tweet about the following topic:
            "${idea}"
            
            The tweet should be concise, intriguing, and formatted to **maximize engagement**.
          `,
        }
      ],
      max_tokens: 60,
      temperature: 0.7,
    });

    const draft = response.choices[0].message.content
    return draft || `No draft generated for idea: ${idea}`;
  } catch (error) {
    console.error('OpenAI error:', error);
    return `Failed to generate tweet from idea: ${idea}`;
  }
}