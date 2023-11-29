from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
import telebot
import config

bot = telebot.TeleBot('bot token')

mydb = mysql.connector.connect(
    host="host",
    user="user_name",
    password="pass",
    database="db_name",
)

cursor = mydb.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    surname = f" {message.from_user.last_name}" if message.from_user.last_name else ''
    bot.send_message(message.chat.id,f"Доброго времени суток, {message.from_user.first_name}{surname}. Введите пожалуйста ИНН вашей компании.")


@bot.message_handler(func=lambda message: True)
def get_next(message):
    conn = mydb.cursor()
    user_inn = message.text

    if user_inn == "/help":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Нет документов для оплаты", callback_data='fetch_doc')
        btn2 = types.InlineKeyboardButton("Нужен акт сверки", callback_data='fetch_act')
        btn3 = types.InlineKeyboardButton("Иной вопрос", callback_data='another_question')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,'выберите один из следующих вопросов, который мешает вам урегулировать задолженность по договорам',reply_markup=markup)
        return
    else:
        conn.execute("SELECT УФПС FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваш УФПС: " + str(result[0]))
        else:
            bot.send_message(message.chat.id,"Информация об организации, которую вы представляете отсутствует в базе данных должников АО Почта россии. Проверьте правильность ввода и нажмите /start, чтобы попробовать еще раз")
        return

        conn.execute("SELECT ОДЗ FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваше ОДЗ: " + str(result[0]))

        conn.execute("SELECT ПДЗ FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваше ПДЗ: " + str(result[0]))


        conn.execute("SELECT НомерДоговора FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваш Номер Договора: " + str(result[0]))


        conn.execute("SELECT ДниПросрочкиПА FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "У вас: " + str(result[0]) + " дней просрочки")


        conn.execute("SELECT Должник FROM able WHERE ИННдолжника = %s", (user_inn,))
        result = conn.fetchone()
        if result:
            bot.send_message(message.chat.id, "Ваша компания: " + str(result[0]))
        # conn.close()

    bot.send_message(message.chat.id, 'введите /help, чтобы получить нужные вам документы или задать вопрос поддержке')


@bot.callback_query_handler(func=lambda callback: callback.data == 'fetch_doc')
def greets(data):
    if isinstance(data, telebot.types.Message):
        i = data.chat.id
    elif isinstance(data, telebot.types.CallbackQuery):
        i = data.message.chat.id

    bot.send_message(i, 'you!', parse_mode='HTML')

@bot.callback_query_handler(func=lambda callback: callback.data == 'fetch_act')
def greets(data):
    if isinstance(data, telebot.types.Message):
        i = data.chat.id
    elif isinstance(data, telebot.types.CallbackQuery):
        i = data.message.chat.id
    bot.send_message(i, 'are!', parse_mode='HTML')

@bot.callback_query_handler(func=lambda callback: callback.data == 'another_question')
def greets(data):
    if isinstance(data, telebot.types.Message):
        i = data.chat.id
    elif isinstance(data, telebot.types.CallbackQuery):
        i = data.message.chat.id
    bot.send_message(i, 'good', parse_mode='HTML')
    
bot.polling(none_stop=True)
