import os
from dotenv import load_dotenv
import openai
import telebot
from datetime import datetime
import sys

# Загрузка переменных окружения из файла .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN должна быть установлена")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY должна быть установлена")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Словарь с днями рождения
birthdays = {
    "Бозорова Ф": "27 декабря",
    "Курбонова М": "15 март",
    "Азимова Л": "31 август",
    "Нурмаматова Л": "30 апрель",
    "Темирова": "29 апрель",
    "Умаров Ж": "31 март",
    "Рахмонов Ф": "6 март",
    "Нафиса": "12 ноябрь",
    "Кодирова x": "5 декабрь",
    "Жумаева Диличка": "1 ноябрь",
    "Мочичехра": "23 июнь",
    "Гуличка": "19 май",
    "Мурод": "31 август",
    "Абдуллаев": "30 август",
    "Санжар": "8 февраль",
    "Элбек": "22 август",
    "Аминов": "10 август",
    "Исроил": "14 январь",
    "Навбахор": "29 март",
    "Бобир": "28 февраль",
    "Сирож": "12 август",
    "Гулбахор": "23 апрель",
    "Элёр": "10 декабрь",
    "Мохигул": "25 март"
}

# Текст поздравления
BIRTHDAY_MESSAGE = (
    "Ассалому алайкум! 🌟\n\n"
    "Бугун сиз учун махсус кун – туғилган кунингиз муборак бўлсин! 🎉 Шундай улуғ кунларда сизга барча эзгуликлар, "
    "соғлиқ-саломатлик, тинчлик-фаровонлик ва албатта, бахту саодат ёр бўлсин!\n\n"
    "Сизнинг ҳаётингизга мўъжизалар билан тўлсин, ҳар бир кунгизни янада ёрқин ва файзли ўтказишингизга тилакдошмиз. "
    "Дўстларингиз ва яқинларингиз сиз билан фахрлансинлар.\n\n"
    "Янги ёшингизда барча орзу-ниятларингиз рўёбга чиқсин ва сизга бериладиган имкониятлар чексиз бўлсин!\n\n"
    "Сизга чин дилдан бахт, омад, ривожланиш ва энг муҳими, ўша асл инсоний қадриятларни сақлаб қолишингизни тилайман. "
    "Қарши олинган ҳар бир янги кун сизнинг энг яхши кунларингиздан бўлсин!\n\n"
    "Туғилган кунингиз яна бир бор муборак бўлсин! 🎂✨\n"
    "Хурмат билан синфдошлар!!"
)

# Проверка на дни рождения
def check_birthdays():
    today = datetime.now().strftime("%-d %B").lower()
    for name, birthday in birthdays.items():
        if birthday.lower() == today:
            send_birthday_greeting(name)

def send_birthday_greeting(name):
    personalized_message = f"Хурматли {name},\n\n{BIRTHDAY_MESSAGE}"
    bot.send_message(chat_id="1946744681", text=personalized_message)

# Обработка сообщений, начинающихся с *B
@bot.message_handler(func=lambda message: message.text.startswith("*B"))
def handle_gpt_query(message):
    user_input = message.text[2:].strip()  # Убираем префикс *B
    response = get_gpt_response(user_input)
    bot.reply_to(message, response)

def get_gpt_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Или "gpt-4", если у вас есть доступ к GPT-4
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "Извините, произошла ошибка при обработке вашего запроса."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_birthdays":
            check_birthdays()
    else:
        bot.polling()
