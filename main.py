from config import telegram_token, db_host, db_user, db_password, db_name, db_port
import telebot
import time
import datetime
from multiprocessing import *
#from multiprocessing.context import Process
import schedule
#global USER_ID
#USER_ID = 0

bot =telebot.TeleBot(telegram_token)










@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, f'Нажали start {message.chat.id}')
    bot.register_next_step_handler(msg, start_process(msg))

def start_process(msg):  # Запуск Process
    global USER_ID
    USER_ID = msg.chat.id
    p1 = Process(target=start_schedule(USER_ID), args=()).start()

def start_schedule(USER_ID):
    schedule.every(10).seconds.do(send_message1)
    while True:  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)

def send_message1():
    bot.send_message(USER_ID, 'Отправка сообщения по времени')


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        pass


# schedule.every().day.at("11:02").do(send_message1)
# while True:  # Запуск цикла
#     schedule.run_pending()
#     time.sleep(1)

#
# telebot.apihelper.proxy = {'PROXY'}
#
#
#
#
# def start_process():  # Запуск Process
#     p1 = Process(target=P_schedule.start_schedule, args=()).start()
#
#
# class P_schedule():  # Class для работы с schedule
#     def start_schedule():  # Запуск schedule
#         ######Параметры для schedule######
#         schedule.every().day.at("11:02").do(P_schedule.send_message1)
#         schedule.every(1).minutes.do(P_schedule.send_message2)
#         ##################################
#
#         while True:  # Запуск цикла
#             schedule.run_pending()
#             time.sleep(1)
#
#     ####Функции для выполнения заданий по времени
#     def send_message1():
#         bot.send_message(USER_ID, 'Отправка сообщения по времени')
#
#     def send_message2():
#         bot.send_message(USER_ID, 'Отправка сообщения через определенное время')
#     ################


# ###Настройки команд telebot#########
# @bot.message_handler(commands=['start'])
# def start(message):
#     USER_ID = message.from_user.id
#     bot.send_message(message.chat.id, 'Нажали start')


#####################

#
# if __name__ == '__main__':
#     start_process()
#     try:
#         bot.polling(none_stop=True)
#     except:
#         pass

