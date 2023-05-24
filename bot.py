import telebot
from telebot import types
from datetime import date
import datetime
import psycopg2

conn = psycopg2.connect(database="bot", user="postgres", password="PelmeN57a", host="localhost", port="5432")
cursor = conn.cursor()


curr_date = date.today()
current_date_string = curr_date.strftime('%m,%d,%y')
curr_week = datetime.date(int(current_date_string[6:8]), int(current_date_string[0:2]), int(current_date_string[3:5])).isocalendar().week
token = '5806758604:AAGp2gxKg1VmtMaysIMymLOPKLqAfD1uU8M'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/help", "/week", "/mtuci")
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница", "Суббота")
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я могу: \nПоказать расписание на понедельник по команде "Понедельник";\nПоказать расписание на вторник по команде "Вторник"; \nПоказать расписание на среду по команде "Среда"; \nПоказать расписание на четверг по команде "Четверг"; \nПоказать расписание на пятницу по команде "Пятница"; \nПоказать расписание на субботу по команде "Суббота"; \nПоказать расписание на текущую неделю по команде "Расписание на текущую неделю"; \nПоказать расписание на следующую неделю по команде "Расписание на следующую неделю"; \nПоказать какая неделя по команде "/week"; \nПоказать ссылку на сайт по команде "/mtuci"; \nПомочь по команде "/help" \n')

@bot.message_handler(commands=['week'])
def start_message(message):
    if curr_week % 2 == 0:
        bot.send_message(message.chat.id, 'Чётная')
    else:
        bot.send_message(message.chat.id, 'Нечётная')


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def answer(message):

    if message.text.lower() == "понедельник":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Понедельник' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Понедельник\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Понедельник' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Понедельник\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "вторник":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Вторник' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' +' '
                result = result +'\n_____\n'
            result = 'Вторник\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Вторник' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' +' '
                result = result +'\n_____\n'
            result = 'Вторник\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "среда":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Среда' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Среда\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Среда' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Среда\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "четверг":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Четверг' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Четверг\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Четверг' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Четверг\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "пятница":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Пятница' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Пятница\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Пятница' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Пятница\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "суббота":
        if curr_week % 2 == 0:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Суббота' AND ch=2 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Суббота\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)
        else:
            cursor.execute("SELECT name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE day LIKE 'Суббота' AND ch=1 ORDER BY start_time")
            query = cursor.fetchall()
            result = ''
            for tuple in query:
                for string in tuple:
                    result = result + f'{string}' + ' '
                result = result + '\n_____\n'
            result = 'Суббота\n' + '_____\n' + result
            bot.send_message(message.chat.id, result)

    if message.text.lower() == "расписание на текущую неделю":
        if curr_week % 2 == 0:
            day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            res = {d: [] for d in day}
            cursor.execute("SELECT day, name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE ch=2 ORDER BY start_time")
            for i in cursor.fetchall():
                if i[0] == 'Понедельник':
                    res["Понедельник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Вторник':
                    res["Вторник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Среда':
                    res["Среда"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Четверг':
                    res["Четверг"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Пятница':
                    res["Пятница"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Суббота':
                    res["Суббота"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
            for i in res:
                bot.send_message(message.chat.id, i + res[i][0] + (res[i][1] if len(res[i]) > 1 else "") + (
                    res[i][2] if len(res[i]) > 2 else "") + (res[i][3] if len(res[i]) > 3 else "") + "\n_____\n")


        else:
            day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            res = {d: [] for d in day}
            cursor.execute("SELECT day, name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE ch=1 ORDER BY start_time")
            for i in cursor.fetchall():
                if i[0] == 'Понедельник':
                    res["Понедельник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Вторник':
                    res["Вторник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Среда':
                    res["Среда"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Четверг':
                    res["Четверг"].append('\n______' + '\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Пятница':
                    res["Пятница"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Суббота':
                    res["Суббота"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
            for i in res:
                bot.send_message(message.chat.id, i + res[i][0] + (res[i][1] if len(res[i])>1 else "") + (res[i][2] if len(res[i])>2 else "") + (res[i][3] if len(res[i])>3 else "") + "\n_____\n")

    if message.text.lower() == "расписание на следующую неделю":
        if curr_week % 2 == 0:
            day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            res = {d: [] for d in day}
            cursor.execute("SELECT day, name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE ch=1 ORDER BY start_time")
            for i in cursor.fetchall():
                if i[0] == 'Понедельник':
                    res["Понедельник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Вторник':
                    res["Вторник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Среда':
                    res["Среда"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Четверг':
                    res["Четверг"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Пятница':
                    res["Пятница"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Суббота':
                    res["Суббота"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
            for i in res:
                bot.send_message(message.chat.id, i + res[i][0] + (res[i][1] if len(res[i]) > 1 else "") + (
                    res[i][2] if len(res[i]) > 2 else "") + (res[i][3] if len(res[i]) > 3 else "") + "\n_____\n")

        else:
            day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            res = {d: [] for d in day}
            cursor.execute("SELECT day, name_s, room_numb, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s INNER JOIN teacher ON subject.id_s=teacher.sub WHERE ch=2 ORDER BY start_time")
            for i in cursor.fetchall():
                if i[0] == 'Понедельник':
                    res["Понедельник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Вторник':
                    res["Вторник"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Среда':
                    res["Среда"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Четверг':
                    res["Четверг"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Пятница':
                    res["Пятница"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
                elif i[0] == 'Суббота':
                    res["Суббота"].append('\n_____\n' + str(i[1]) + '   ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '\n')
            for i in res:
                bot.send_message(message.chat.id, i + res[i][0] + (res[i][1] if len(res[i]) > 1 else "") + (
                    res[i][2] if len(res[i]) > 2 else "") + (res[i][3] if len(res[i]) > 3 else "") + "\n_____\n")
    if message.text.lower() not in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "расписание на текущую неделю", 'расписание на следующую неделю']:
        bot.send_message(message.chat.id, 'Извините, я вас не понял')

bot.infinity_polling()






