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






def start_schedule():
    schedule.every(10).seconds.do(send_message1)
    while True:  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)



@bot.message_handler(commands=['start'])
def start(message):
    #USER_ID = message.from_user.id
    #USER_ID = message.chat.id
    bot.send_message(message.chat.id, f'Нажали start {message.chat.id}')
    msg = bot.reply_to(message, "fабвг")
    bot.register_next_step_handler(msg, start_process(msg))
    #start_process()

def start_process(msg):  # Запуск Process
    global USER_ID
    USER_ID = msg.chat.id
    print(USER_ID)
    p1 = Process(target=start_schedule, args=()).start()

def send_message1():
    #global USER_ID
    print(USER_ID)
    bot.send_message(USER_ID, 'Отправка сообщения по времени')
    #94046674

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

