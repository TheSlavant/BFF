import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

system_prompt = """INSERT YOUR PROMPT HERE"""

client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize a dictionary to keep track of chat contexts
chat_contexts = {}

async def generate_response(chat_id, message):
    # Ensure the chat has an entry in the chat_histories dictionary
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = [{"role": "system", "content": system_prompt}]
    
    # Append the new user message to the history
    chat_contexts[chat_id].append({"role": "user", "content": message})
    
    # Generate response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=chat_contexts[chat_id],
        max_tokens=256,
        temperature=1
    )
    
    # Append the bot response to the history
    bot_message = response.choices[0].message.content
    chat_contexts[chat_id].append({"role": "assistant", "content": bot_message})
    
    return bot_message

# Function to handle text messages
async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_text = update.message.text
    
    # Check if the message is "forget"
    if message_text.strip().lower() == "forget":
        # Clear the chat context for this user
        chat_contexts.pop(chat_id, None)
        await context.bot.send_message(chat_id=chat_id, text="I've forgotten our previous conversation.")
        return
    
    # Generate a response to the incoming text message
    response_message = await generate_response(chat_id, message_text)
    
    # Send the response back to the user
    await context.bot.send_message(chat_id=chat_id, text=response_message)

# Main function to start the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()