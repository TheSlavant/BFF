# BFF: A real-life implementation of Samantha from "Her"

Now you can have a Samantha of your own! 

BFF is an open-source initiative to create a personal AI assistant similar to the OS'es from the movie "Her". Like Samantha, your BFF will tailor its personality to you, be incredibly insightful, and will truly understand you. It will feel like talking to a smart, caring, and down-to-earth friend.

## Modules

![BFF modules](/images/bff-modules.png "BFF modules")

## Use Cases

We are building BFF to be good at things ChatGPT can't do well. Here are some things you will be able to do with BFF:

- Brainstorm ideas
- Look at a problem from a new angle
- Ask for advice
- Find gaps in your thinking
- Set the mood for the day
- Joke around

## Getting Started

Today, you can interact with BFF through a Telegram bot, making it feel like you're talking to a friend. We're also working on new interfaces, and we welcome contributions. If you are interested in building the best interface for personal AI, join the Discord and let's build together.

### Setting up your Telegram bot

**Step 1: Clone the BFF project**
- Clone the BFF project repository to your local machine: `git clone https://github.com/TheSlavant/BFF.git`

**Step 2: Create your bot**
- Open Telegram and search for "BotFather".
- Send "/newbot" to BotFather and follow the prompts to create your bot. Choose a name and a username that ends with ‘bot’ (e.g., mybff_bot).
- After creation, BotFather will give you a token. This token allows your application to communicate with the Telegram API. Keep it secure.

**Step 3: Set up your BFF**
- Navigate to `interface/telegram-bot/` in the BFF project.
- Open `bff-telegram-bot.py`. Replace the `TELEGRAM_TOKEN` placeholder with your actual bot token.
- Update the `system_prompt` line in `bff-telegram-bot.py` to include your chosen prompt. Check out the `prompts` directory for prompt ideas you can use.

**Step 4: Run the code and say hi to your BFF**
- Make sure Python and all dependencies are installed. Install any necessary libraries using pip.
- Run your BFF: `python bff-telegram-bot.py`.
- Your BFF is now live on Telegram! Say hi, ask for advice, and have fun.
