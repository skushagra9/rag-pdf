import {Ollama} from "ollama";

const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })



export async function generateTweetDraft(idea: string): Promise<string> {
  try {
    const response = await ollama.chat({
      model: 'llama3.2:latest',
      messages: [
        {
          role: 'system',
          content: `
            You are a highly skilled social media strategist with an innate understanding of what makes tweets go viral. Your goal is to craft tweets that not only spark engagement but also have the potential to trend. You have mastered Twitter's algorithm and know exactly how to:
            - **Engage followers**: Create content that drives replies, retweets, likes, and shares.
            - **Leverage viral elements**: Incorporate trends, humor, relatable content, or a controversial stance (without being offensive).
            - **Maximize visibility**: Use hashtags, mentions, and trending topics to expand reach.
            - **Optimize for 280 characters**: Every word should have purpose—no filler, no fluff.
            - **Craft for personality**: Whether witty, insightful, or thought-provoking, the tweet must feel human and authentic.
            - **Keep urgency when appropriate**: If the topic is news-related, make it timely and eye-catching.
            - **Include a clear call to action (CTA)**: Prompt followers to engage, share, or comment.
    
            **Additional Guidelines**:
            - The tweet should **spark conversation** and encourage discussions.
            - Infuse humor when possible, but don’t sacrifice clarity.
            - Stay away from AI-like phrasing—make it sound like a real person, not a bot.
            - **Make it memorable** and something people would want to share with their own followers.
    
            Your task is to take the given topic and create a **viral-ready tweet** that follows all of these principles.
          `,
        },
        {
          role: 'user',
          content: `
            Create a tweet that has the potential to go viral, based on this idea:
            "${idea}"
    
            The tweet should be intriguing, concise, and highly engaging, designed to encourage retweets, replies, and likes.
          `,
        }
      ],
    });
    
    const draft = response.message.content
    return draft || `No draft generated for idea: ${idea}`;
  } catch (error) {
    console.error('OpenAI error:', error);
    return `Failed to generate tweet from idea: ${idea}`;
  }
}