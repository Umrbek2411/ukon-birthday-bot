# 🎩 UKON Birthday Bot

Telegram bot that guesses your birthday using a classic math trick. Built with Python, deployed with Docker, and fully multilingual (Uzbek / Russian / English).

## ✨ Features

- **Interactive step-by-step flow** — the bot walks the user through 7 simple arithmetic steps one at a time via `ConversationHandler` states, instead of dumping all instructions at once
- **Multilingual support** — language selection via inline keyboard buttons (🇺🇿 O'zbekcha / 🇷🇺 Русский / 🇬🇧 English), with all bot messages translated
- **Math trick engine** — reconstructs the user's birth month and day from a single final number using the classic encoding trick:
  ```
  ((month × 5 + 6) × 4 + 9) × 5 + day − 165  =  month × 100 + day
  ```
- **Input validation** — gracefully handles non-numeric input and out-of-range results
- **Dockerized deployment** — runs as an isolated container with automatic restart on failure
- **Environment-based configuration** — bot token kept out of source control via `.env` + `python-dotenv`

## 🛠️ Tech Stack

- **Python 3.12**
- **python-telegram-bot** v21 (async, `Application` / `ConversationHandler` / `CallbackQueryHandler`)
- **python-dotenv** for configuration
- **Docker** & **Docker Compose** for containerized deployment

## 📂 Project Structure

```
ukon-birthday-bot/
├── bot.py                 # Main bot logic (conversation flow, math trick, translations)
├── requirements.txt       # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Compose service definition
├── .gitignore
└── README.md
```

## 🚀 Running Locally

### Prerequisites
- Docker Desktop installed and running
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Umrbek2411/ukon-birthday-bot.git
   cd ukon-birthday-bot
   ```

2. Create a `.env` file in the project root:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

3. Build and run with Docker Compose:
   ```bash
   docker compose up -d --build
   ```

4. Check logs:
   ```bash
   docker compose logs -f
   ```

5. Open your bot in Telegram and send `/start`.

### Running without Docker

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

## 🧠 How the Math Trick Works

The bot never asks for your birth month or day directly. Instead, it asks you to perform a sequence of arithmetic operations, and reconstructs the date purely from the final number:

| Step | Operation |
|------|-----------|
| 1 | Multiply birth month (1–12) by 5 |
| 2 | Add 6 |
| 3 | Multiply by 4 |
| 4 | Add 9 |
| 5 | Multiply by 5 |
| 6 | Add birth day (1–31) |
| 7 | Subtract 165 |

The final result always equals `month × 100 + day`, so the bot decodes it with simple integer division and modulo.

## 📄 License

MIT

## 👤 Author

**Umrbek** — part of the **UKON** project portfolio.
- GitHub: [@Umrbek2411](https://github.com/Umrbek2411)