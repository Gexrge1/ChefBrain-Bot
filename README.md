# 🍳 ChefBrain BOT

A Telegram bot that uses AI to suggest recipes, generate cooking instructions, and help users discover meals based on their available ingredients or food preferences.

## Features

- 🧠 Generate random recipe suggestions.
- 👨‍🍳 Generate complete recipes using AI.
- 📝 Suggest recipes based on user-provided ingredients or descriptions.
- ⌨️ Navigate through the bot using inline and reply keyboards.
- ❓ Built-in help and instructions.

## Tech Stack

- Python
- [aiogram](https://github.com/aiogram/aiogram) — Telegram Bot API framework
- [Groq](https://groq.com/) — AI-powered recipe generation
- `python-dotenv` — Environment variable management

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:

   ```bash
   pip install aiogram groq python-dotenv
   ```

3. Create a `.env` file:

   ```env
   BOT_TOKEN=your_telegram_bot_token
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the bot:

   ```bash
   python bot.py
   ```

## Development Checklist

- [x] Suggesting random recipes to users
- [x] Full generation of suggested recipes
- [x] Inline keyboard logic for recipes
- [x] Reply keyboard logic for the main menu and recipes
- [x] Generation of recipes based on user-provided input
- [ ] Favourite recipes
- [ ] User preferences (allergies, diet, spice level)
- [ ] Database integration
- [ ] Multi-language support
- [ ] Bot startup information
