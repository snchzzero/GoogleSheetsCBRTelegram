from config import telegram_token, db_host, db_user, db_password, db_name, db_port
import telebot
import time
import datetime
from multiprocessing import *
import schedule
from script import db_google_sheets

bot =telebot.TeleBot(telegram_token)

def start_process(msg):  # Запуск Process
    global USER_ID
    USER_ID = msg.chat.id
    global p1
    p1 = Process(target=start_schedule(USER_ID), args=()).start()




def start_schedule(USER_ID):
    l1 = db_google_sheets()
    message_string = "Cрок поставки прошел по следующим позициям: (сортировка по дате) \n"
    for l in l1:
        message_string += f"№{l[0]}, Заказ №{l[1]}, Срок: {l[2]} \n"
    bot.send_message(USER_ID, message_string)

    schedule.every(10).seconds.do(send_message1)
# schedule.every().day.at("11:02").do(send_message1)
    while True:  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)

def send_message1():
    bot.send_message(USER_ID, 'Отправка сообщения по времени')



@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, f'Нажали start {message.chat.id}')
    bot.register_next_step_handler(msg, start_process(msg))

@bot.message_handler(commands=['stop'])
def start(message):
    msg = bot.send_message(message.chat.id, f'Расылка уведомлений выключена')
    #p1.terminate()
    #p1.close()
    p1.join()

    #schedule.cancel_job(start_schedule(USER_ID))





if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        pass

