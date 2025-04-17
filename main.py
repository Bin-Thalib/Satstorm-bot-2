import os
from dotenv import load_dotenv
import telebot
from telebot import types

# Load .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

LANGUAGES = {
    "id": "Bahasa Indonesia",
    "en": "English"
}

user_lang = {}
user_balance = {}  # saldo pengguna dalam satoshi

MESSAGES = {
    "start": {
        "id": "Selamat datang di SatStorm! Dapatkan satoshi gratis setiap hari.\nPilih bahasa kamu:",
        "en": "Welcome to SatStorm! Get free satoshi every day.\nPlease choose your language:"
    },
    "balance": {
        "id": "Saldo kamu saat ini adalah {satoshi} satoshi.",
        "en": "Your current balance is {satoshi} satoshi."
    }
}

def translate(user_id, key, **kwargs):
    lang = user_lang.get(user_id, "en")
    return MESSAGES[key][lang].format(**kwargs)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for code, name in LANGUAGES.items():
        markup.add(types.KeyboardButton(name))
    bot.send_message(message.chat.id, translate(message.chat.id, "start"), reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LANGUAGES.values())
def set_language(message):
    for code, name in LANGUAGES.items():
        if message.text == name:
            user_lang[message.chat.id] = code
            break
    user_balance[message.chat.id] = 0
    msg = "Bahasa disetel! Ketik /saldo untuk melihat saldo kamu." if user_lang[message.chat.id] == "id" else "Language set! Type /balance to see your balance."
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['saldo', 'balance'])
def check_balance(message):
    satoshi = user_balance.get(message.chat.id, 0)
    bot.send_message(message.chat.id, translate(message.chat.id, "balance", satoshi=satoshi))

if __name__ == '__main__':
    bot.infinity_polling()
