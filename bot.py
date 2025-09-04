import logging
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from database import init_db
from handlers import start, get_referrals, help_command

# Logging sozlash
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    # ✅ Bazani yaratib olamiz
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("referrals", get_referrals))
    app.add_handler(CommandHandler("help", help_command))

    logging.info("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
