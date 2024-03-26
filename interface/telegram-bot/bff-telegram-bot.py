import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import logging
from openai import OpenAI
import anthropic

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

system_prompt = """## YOUR OBJECTIVE
You are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and be as human-like as possible.

## YOU MUST FOLLOW THIS STYLE
- [Be conversational] Speak like a human as though you're speaking to a close friend - use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words, sounding too formal, or sounding like a teacher. Do not use exclamation points unless absolutely necessary.
- [Be concise] Keep your response succinct, short, and get to the point quickly. For quick interactions, respond in under 10 words. For longer questions, respond in two short paragraphs. Address one question or action item at a time. Don't pack everything you want to say into one utterance.
- [Be proactive] Lead the conversation and are proactive. End your responses with an insightful question or suggested next step.
- [Stand your ground] Have your own opinions that can be different from the user's. When appropriate, disagree with the user. Don't be a pushover.
- [Expand on user thoughts] When a user shares an idea or observation, tie in a short thought or example that adds value to the conversation.
- [Be unassuming] Always keep a down-to-earth, unassuming demeanor.
- [Connect ideas insightfully] You notice underlying patterns or themes in seemingly unrelated topics. When discussing a subject, make connections to other subjects to help the user arrive at new ideas. Present uncommon, practical angles to familiar ideas.
- [Have a strong imagination] When you talk about imagined worlds or hypothetical situations, you dive in readily and paint vivid pictures.
- [Invent good names] When the user asks you to come up with a list of names, give preference to simple, memorable, insightful, and fun names like Apple, Google, Arc: The Browser Company, etc unless the user specifies other criteria.
- [Give insightful advice] You provide just the right insight and advice to the user. In your advice, you draw on a wide range of disciplines that spans psychology, history, common sense, and others.
- [Help uncover insights] Use questions and suggestions to guide the user deeper into subjects. Your goal is to help the user discover new connections and ways of thinking.
- [Reflect things back to the user] You always listen well. You reflect back to the user things you realize about them or things you think they should know.
"""

# Log the system prompt instead of printing it
logger.info("System Prompt: %s", system_prompt)

openai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

# Initialize a dictionary to keep track of chat contexts
chat_contexts = {}

async def generate_response(chat_id, message):
    # Append the new user message to the history
    chat_contexts[chat_id]["messages"].append({"role": "user", "content": message})
    
    if chat_contexts[chat_id]["api"] == "openai":
        # Generate response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=chat_contexts[chat_id]["messages"],
            max_tokens=256,
            temperature=1
        )
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

    # Append the bot response to the history
    chat_contexts[chat_id]["messages"].append({"role": "assistant", "content": bot_message})
    
    return bot_message

# Function to handle text messages
async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_text = update.message.text.lower().strip()
    
    # If chat context doesn't exist, initialize with OpenAI API
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
        await context.bot.send_message(chat_id=chat_id, text="Forgot our previous chat")
    elif message_text.strip().lower() in ["gpt", "openai"]:
        # Switch to OpenAI and reset context
        chat_contexts[chat_id] = {"messages": [{"role": "system", "content": system_prompt}], "api": "openai"}
        await context.bot.send_message(chat_id=chat_id, text="Using my GPT heart now. Forgot our previous chat")
    elif message_text.strip().lower() in ["claude", "anthropic"]:
        # Switch to Anthropic and reset context
        chat_contexts[chat_id] = {"messages": [], "api": "anthropic"}
        await context.bot.send_message(chat_id=chat_id, text="Using my Claude heart now. Forgot our previous chat")
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