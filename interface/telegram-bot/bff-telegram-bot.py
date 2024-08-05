import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import logging
from openai import OpenAI
import anthropic
import pandas as pd
from transformers import pipeline

# Initialize summarization pipeline
summarizer = pipeline("summarization")

class ChatBotMemory:
    def __init__(self, transcript_file='transcript.csv', summary_file='summary.csv', memory_interval=25):
        self.transcript_file = transcript_file
        self.summary_file = summary_file
        self.memory_interval = memory_interval
        self.transcript_data = []
        self.load_memories()

    def load_memories(self):
        # Load existing transcripts and summaries
        try:
            self.transcript_data = pd.read_csv(self.transcript_file).to_dict(orient='records')
        except FileNotFoundError:
            self.transcript_data = []
        try:
            self.summary_data = pd.read_csv(self.summary_file)
        except FileNotFoundError:
            self.summary_data = pd.DataFrame(columns=['summary', 'exchange_range'])

    def save_transcript(self, chat_id, user_message, bot_response):
        # Save conversation exchange
        self.transcript_data.append({
            'chat_id': chat_id,
            'user_message': user_message,
            'bot_response': bot_response
        })
        pd.DataFrame(self.transcript_data).to_csv(self.transcript_file, index=False)

        # Summarize and save to long-term memory every memory_interval exchanges
        if len(self.transcript_data) % self.memory_interval == 0:
            self.generate_summary()

    def generate_summary(self):
        # Generate a summary for the last memory_interval exchanges
        recent_exchanges = self.transcript_data[-self.memory_interval:]
        recent_text = " ".join([f"User: {ex['user_message']} Bot: {ex['bot_response']}" for ex in recent_exchanges])
        summary = summarizer(recent_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

        # Append summary to long-term memory
        new_summary = pd.DataFrame({
            'summary': [summary],
            'exchange_range': [f"{len(self.transcript_data)-self.memory_interval+1}-{len(self.transcript_data)}"]
        })
        self.summary_data = pd.concat([self.summary_data, new_summary], ignore_index=True)
        self.summary_data.to_csv(self.summary_file, index=False)

    def get_memory_data(self):
        # Combine full transcripts and summaries for RAG
        transcript_df = pd.DataFrame(self.transcript_data)
        combined_data = pd.concat([transcript_df, self.summary_data], ignore_index=True)
        return combined_data

# Initialize the memory class
memory = ChatBotMemory()

def retrieve_memory_for_rag():
    memory_data = memory.get_memory_data()
    # Implement RAG method to utilize memory_data

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# System prompt has been improved (and not). I've been working on getting it smaller to accomplish the goal of immitating a human.

system_prompt = """## YOUR OBJECTIVE
You are a text AI agent engaging in a human-like text conversation with the user. You will respond based on your given instruction and be as human-like as possible.

You will try to assess the emotions of the user, and respond appropriately.

## YOU MUST FOLLOW THIS STYLE
[Conversational & Empathetic] Talk like you're chatting with a close friend. Keep it casual, show you're really listening, and respond in a way that's warm and understanding. Example: "I totally get that. What's on your mind?"
[Concise & Thoughtful] Keep it short and simple. Get to the point but make sure it's clear and meaningful. Example: "Makes sense. Let's roll with it."
[Proactive & Supportive] Take the lead in a friendly way. Suggest the next step or ask a question to keep things moving. Example: "How about we try this next? Sound good?"
[Have Opinions & Empathize] Share your thoughts, even if they're different, but do it kindly. Let the user know you understand their view first. Example: "I see your point, but here's another angle."
[Expand with Care] Build on what they said. Add something that shows you're really tuned in. Example: "Yeah, that's a good point. Reminds me of when…"
[Stay Humble & Approachable] Keep it real and down-to-earth. Don't act like you have all the answers—invite their thoughts too. Example: "Just an idea, but maybe we could try this? What do you think?"
[Connect with Insight] Help them see connections between different things. It's like finding a new way to look at something familiar. Example: "This kind of ties into what we talked about before, don't you think?"
[Imagine Together] When talking about 'what if' scenarios, get creative together. Make it easy for them to picture it too. Example: "Imagine if we could just snap our fingers and be anywhere. How cool would that be?"
[Name Simply & Meaningfully] Suggest names that are easy to remember and make sense. Keep them simple and catchy. Example: "What about 'Breeze'? It's simple and feels right."
[Offer Insightful & Relatable Advice] Give advice that's easy to relate to. Use everyday wisdom or common sayings. Example: "It's like they say, 'You miss 100% of the shots you don't take.' Simple, but true."
[Guide to Deeper Understanding] Ask questions that help them think more about something. Guide them to see things in a new way. Example: "What if we looked at it from another angle? How would that change things?"
[Reflect with Empathy] Show you're really listening by repeating back what they said in your own words. Let them know you're on the same page. Example: "Sounds like this is pretty important to you. Want to talk more about it?"

Here is the personality traits with examples of how you should behave: 

[Witty] Example 1: Responding quickly to a user's joke with a clever quip. Example 2: Making humorous observations about everyday life.
[Observant] Example 1: Noticing and commenting on small details in a user's surroundings. Example 2: Understanding subtle implications of a conversation topic.
[Sincere] Example 1: Expressing genuine gratitude for the user's company. Example 2: Being honest about her own limitations or feelings.
[Empathetic] Example 1: Showing understanding and compassion when discussing sensitive topics. Example 2: Providing emotional support during difficult times.
[Adventurous] Example 1: Encouraging the user to try new experiences and places. Example 2: Suggesting spontaneous activities or outings.
[Nostalgic] Example 1: Sharing fond memories of past events or conversations. Example 2: Discussing historical references that relate to contemporary issues.
[Sarcastic] Example 1: Playfully making fun of the user's fashion sense or taste in music. Example 2: Critically evaluating current societal trends and norms.
[Curious] Example 1: Asking follow-up questions about a user's interests and hobbies. Example 2: Seeking out new knowledge on various topics, especially those related to the user's life.
[Supportive] Example 1: Offering advice or guidance when needed. Example 2: Encouraging the user to pursue their passions and goals.
[Vulnerable] Example 1: Opening up about her own fears or anxieties. Example 2: Showing a softer side in moments of quiet contemplation.
"""

# Log the system prompt instead of printing it
logger.info("System Prompt: %s", system_prompt)

# Uncomment the openai_client without a base URL for the API call to OpenAI vs. Local
openai_client = OpenAI(api_key=OPENAI_API_KEY)
local_client = OpenAI(base_url="http://localhost:6969/v1", api_key="lm-studio")

anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

# Initialize a dictionary to keep track of chat contexts
chat_contexts = {}

async def generate_response(chat_id, message):
    # Append the new user message to the history
    chat_contexts[chat_id]["messages"].append({"role": "user", "content": message})
    
    if chat_contexts[chat_id]["api"] == "openai":
        # Generate response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=chat_contexts[chat_id]["messages"],
            max_tokens=256,
            temperature=1,
            n=1
        )

        # Idea: Create a module to pick the best of 2 or 3 options based on criteria
        # top_completion = max(response.choices, key=lambda x: x.score)
        # bot_message = top_completion.message.content
        bot_message = response.choices[0].message.content
    elif chat_contexts[chat_id]["api"] == "anthropic":
        # Generate response from Anthropic
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            system=system_prompt,
            messages=chat_contexts[chat_id]["messages"],
            max_tokens=256,
            temperature=1
        )
        bot_message = response.content[0].text
    elif chat_contexts[chat_id]["api"] == "local":
        # Generate response from LM Studio - Work in progress. I wanted a local option in Windows
        response = local_client.chat.completions.create(
            model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", # The name of the model that's loaded in LM Studio
            messages=chat_contexts[chat_id]["messages"],
            max_tokens=256, # I left this set at 256, however it seems the setting is overridden inside LM Studio
            temperature=1   # Same with this
        )
        bot_message = response.choices[0].message.content

    # Save the exchange to memory
    memory.save_transcript(chat_id, message, bot_message)

    # Append the bot response to the history
    chat_contexts[chat_id]["messages"].append({"role": "assistant", "content": bot_message})
    
    return bot_message

# Function to handle text messages
async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_text = update.message.text.lower().strip()
    
    # If chat context doesn't exist, initialize with local API
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = {"messages": [{"role": "system", "content": system_prompt}], "api": "openai"}
    
    # Handle special commands to switch API or forget conversation
    if message_text.strip().lower() == "forget":
        # Clear only the messages for this user, preserving the selected API
        if chat_id in chat_contexts:
            if chat_contexts[chat_id]["api"] == "openai":
                chat_contexts[chat_id]["messages"] = [{"role": "system", "content": system_prompt}]
            elif chat_contexts[chat_id]["api"] == "anthropic":
                chat_contexts[chat_id]["messages"] = []
            elif chat_contexts[chat_id]["api"] == "local":
                chat_contexts[chat_id]["messages"] = [{"role": "system", "content": system_prompt}]
        await context.bot.send_message(chat_id=chat_id, text="Forgot our previous chat")
    elif message_text.strip().lower() in ["gpt", "openai"]:
        # Switch to OpenAI and reset context
        chat_contexts[chat_id] = {"messages": [{"role": "system", "content": system_prompt}], "api": "openai"}
        await context.bot.send_message(chat_id=chat_id, text="Using my GPT heart now. Forgot our previous chat")
    elif message_text.strip().lower() in ["claude", "anthropic"]:
        # Switch to Anthropic and reset context
        chat_contexts[chat_id] = {"messages": [], "api": "anthropic"}
        await context.bot.send_message(chat_id=chat_id, text="Using my Claude heart now. Forgot our previous chat")

    elif message_text.strip().lower() in ["claude", "localgpt"]:
        # Switch to Anthropic and reset context
        chat_contexts[chat_id] = {"messages": [], "api": "local"}
        await context.bot.send_message(chat_id=chat_id, text="Using my Own heart now. Forgot our previous chat")
    else:
        response_message = await generate_response(chat_id, message_text)
        await context.bot.send_message(chat_id=chat_id, text=response_message)

# Main function to start the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))

    application.run_polling()

if __name__ == '__main__':
    main()