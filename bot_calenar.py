import telebot
import calendar
import datetime
from calend import add_event, get_month, get_week, get_day, add_link
from export_functions import export_to_pdf
from calend import timegm
from calend import Calendar


TOKEN = '1956657569:AAHi0krK6jv2xjZ7oK235G1SYvoQxrSmj18'
bot = telebot.TeleBot(TOKEN)

# crea una instancia de la clase Calendar
cal = Calendar()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, '¡Bienvenido! Usa /help para ver los comandos disponibles.')

@bot.message_handler(commands=['evento'])
def add_event_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Introduce la fecha en formato YYYY-MM-DD:')
    bot.register_next_step_handler(msg, add_event_step1)

def add_event_step1(message):
    chat_id = message.chat.id
    try:
        date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        event = {'date': date}
        msg = bot.send_message(chat_id, 'Introduce la hora en formato HH:MM (opcional):')
        bot.register_next_step_handler(msg, add_event_step2, event)
    except ValueError:
        bot.send_message(chat_id, 'Fecha inválida. Introduce la fecha en formato YYYY-MM-DD.')
        add_event_handler(message)

def add_event_step2(message, event):
    chat_id = message.chat.id
    try:
        time = datetime.datetime.strptime(message.text, '%H:%M').time()
        event['time'] = time
    except ValueError:
        pass
    msg = bot.send_message(chat_id, '¿Quieres que el evento se repita? (S/N)')
    bot.register_next_step_handler(msg, add_event_step3, event)

def add_event_step3(message, event):
    chat_id = message.chat.id
    if message.text.upper() == 'S':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Día concreto', 'Día cada semana', 'Una vez al mes')
        msg = bot.send_message(chat_id, 'Elige el intervalo de repetición:', reply_markup=markup)
        bot.register_next_step_handler(msg, add_event_step4, event)
    elif message.text.upper() == 'N':
        add_event(event, chat_id)
    else:
        msg = bot.send_message(chat_id, 'Respuesta inválida. ¿Quieres que el evento se repita? (S/N)')
        bot.register_next_step_handler(msg, add_event_step3, event)

def add_event_step4(message, event):
    chat_id = message.chat.id
    if message.text == 'Día concreto':
        msg = bot.send_message(chat_id, 'Introduce la fecha en formato YYYY-MM-DD:')
        bot.register_next_step_handler(msg, add_event_step5, event, 'day')
    elif message.text == 'Día cada semana':
        msg = bot.send_message(chat_id, 'Introduce el día de la semana (0=lunes, 1=martes, etc.):')
        bot.register_next_step_handler(msg, add_event_step5, event, 'week')
    elif message.text == 'Una vez al mes':
        msg = bot.send_message(chat_id, 'Introduce el día del mes (1-31):')
        bot.register_next_step_handler(msg, add_event_step5, event, 'month')
    else:
        msg = bot.send_message(chat_id, 'Respuesta inválida. Elige el intervalo de repetición:')
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Día concreto', 'Día cada semana', 'Una vez al mes')
    bot.send_message(chat_id, 'Elige el intervalo de repetición:', reply_markup=markup)
"""
def add_event_step5(message, event, repeat_interval):
    chat_id = message.chat.id
    try:
        date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError:
        bot.send_message(chat_id, 'Formato de fecha inválido. Introduce la fecha en formato YYYY-MM-DD:')
        return bot.register_next_step_handler(message, add_event_step5, event, repeat_interval)

    if repeat_interval == 'day':
        event.repeat_interval = f'daily:{date}'
    elif repeat_interval == 'week':
        event.repeat_interval = f'weekly:{date.weekday()}'
    elif repeat_interval == 'month':
        event.repeat_interval = f'monthly:{date.day}'
        add_event_step6(message, event)
"""
# define la función add_event_step5
def add_event_step5(message, event, repeat_interval):
    chat_id = message.chat.id
    try:
        date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError:
        bot.send_message(chat_id, 'Formato de fecha inválido. Introduce la fecha en formato YYYY-MM-DD:')
    else:
        # llama al método add_event de la instancia de Calendar
        cal.add_event(date, repeat=repeat_interval)
        add_event_step6(message, event)

def add_event_step6(message, event):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, '¿Quieres añadir un enlace al evento? (responde Sí o No)')
    bot.register_next_step_handler(msg, add_event_step7, event)

def add_event_step7(message, event):
    chat_id = message.chat.id
    if message.text.lower() == 'sí':
        msg = bot.send_message(chat_id, 'Introduce el enlace:')
        bot.register_next_step_handler(msg, add_event_step8, event)
    elif message.text.lower() == 'no':
        add_event_step9(message, event)
    else:
        msg = bot.send_message(chat_id, 'Respuesta inválida. ¿Quieres añadir un enlace al evento? (responde Sí o No)')
        bot.register_next_step_handler(msg, add_event_step7, event)

def add_event_step8(message, event):
    chat_id = message.chat.id
    event.link = message.text
    add_event_step9(message, event)

def add_event_step9(message, event):
    chat_id = message.chat.id
    calend.add_event(event)
    bot.send_message(chat_id, 'Evento añadido al calendario.')
    bot.send_message(chat_id, '¿Quieres añadir otro evento? (responde Sí o No)')
    bot.register_next_step_handler(message, add_event_step1)

@bot.message_handler(commands=['evento'])

def add_event_step1(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Introduce el título del evento:')
    bot.register_next_step_handler(message, add_event_step2)

def add_event_step2(message, event=None):
    chat_id = message.chat.id
    title = message.text
    event = Event(title=title)
    bot.send_message(chat_id, '¿Quieres añadir una descripción al evento? (responde Sí o No)')
    bot.register_next_step_handler(message, add_event_step3, event)

def add_event_step3(message, event):
    chat_id = message.chat.id
    if message.text.lower() == 'sí':
        bot.send_message(chat_id, 'Introduce la descripción:')
        bot.register_next_step_handler(message, add_event_step4, event)
    else:
        add_event_step4(message, event, '')

def add_event_step4(message, event, description=None):
    chat_id = message.chat.id
    if description is None:
        description = message.text
        event.description = description
        bot.send_message(chat_id, '¿Quieres añadir una fecha y hora al evento? (responde Sí o No)')
        bot.register_next_step_handler(message, add_event_step5, event, 'datetime')

def add_event_step5(message, event, event_type):
    chat_id = message.chat.id
    if message.text.lower() == 'sí':
        if event_type == 'datetime':
            bot.send_message(chat_id, 'Introduce la fecha y hora en formato YYYY-MM-DD HH:MM:')
            bot.register_next_step_handler(message, add_event_step6, event)
        elif event_type == 'day':
            bot.send_message(chat_id, 'Introduce la hora en formato HH:MM:')
            bot.register_next_step_handler(message, add_event_step7, event, event_type)
        elif event_type == 'week':
            bot.send_message(chat_id, 'Introduce la hora en formato HH:MM:')
            bot.register_next_step_handler(message, add_event_step7, event, event_type)
        elif event_type == 'month':
            bot.send_message(chat_id, 'Introduce la hora en formato HH:MM:')
            bot.register_next_step_handler(message, add_event_step7, event, event_type)
        else:
            add_event_step8(message, event)

def add_event_step6(message, event):
    chat_id = message.chat.id
    try:
        date_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        event.start_time = date_time
        bot.send_message(chat_id, '¿Quieres añadir una fecha y hora de finalización? (responde Sí o No)')
        bot.register_next_step_handler(message, add_event_step7, event)
    except ValueError:
        bot.send_message(chat_id, 'Formato de fecha y hora incorrecto. Introduce la fecha y hora en formato YYYY-MM-DD HH:MM:')
        bot.register_next_step_handler(message, add_event_step6, event)

def add_event_step7(message, event, event_type):
    chat_id = message.chat.id
    try:
        time = datetime.datetime.strptime(message.text, '%H:%M').time()
        if event_type == 'datetime':
            event.start_time = datetime.datetime.combine(event.start_time.date(), time)
            bot.send_message(chat_id, '¿Quieres añadir una fecha y hora de finalización? (responde Sí o No)')
            bot.register_next_step_handler(message, add_event_step8, event)
        elif event_type == 'day':
            event.start_time = time
            bot.send_message(chat_id, '¿Quieres añadir una hora de finalización? (responde Sí o No)')
            bot.register_next_step_handler(message, add_event_step8, event)
    except ValueError:
        bot.send_message(chat_id, 'Hora inválida. Introduce una hora en formato HH:MM.')
        bot.register_next_step_handler(message, add_event_step7, event, event_type)

def add_event_step8(message, event):
    chat_id = message.chat.id
    bot.send_message(chat_id, '¿Quieres añadir un enlace al evento? (responde Sí o No)')
    bot.register_next_step_handler(message, add_event_step9, event)

def add_event_step9(message, event):
    chat_id = message.chat.id
    if message.text.lower() == 'sí':
        bot.send_message(chat_id, 'Introduce el enlace:')
        bot.register_next_step_handler(message, add_event_step10, event)
    else:
        add_event_step10(message, event, '')

def add_event_step10(message, event, link=None):
    chat_id = message.chat.id
    if link is None:
        link = message.text
    cal = Calendario()
    cal.add_event(date=event.start_time.strftime('%Y-%m-%d'), time=event.start_time.strftime('%H:%M'), repeat=None, link=link)
    bot.send_message(chat_id, 'Evento añadido exitosamente')

@bot.message_handler(commands=['mes'])
def show_monthly_events(message):
    chat_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Este mes', 'Mes siguiente')
    msg = bot.send_message(chat_id, 'Elige el mes que quieres ver:', reply_markup=markup)
    bot.register_next_step_handler(msg, show_monthly_events_step2)


def show_monthly_events_step2(message):
    chat_id = message.chat.id
    if message.text == 'Este mes':
        start_date = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
    elif message.text == 'Mes siguiente':
        start_date = (datetime.datetime.now() + relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
    else:
        bot.send_message(chat_id, 'Respuesta inválida. Elige el mes que quieres ver.')
        return

    events = calend.get_events(start_date, end_date)
    if not events:
        bot.send_message(chat_id, 'No hay eventos programados para este mes.')
        return
    events_text = format_events(events)
    bot.send_message(chat_id, f"Eventos para el mes de {start_date.strftime('%B %Y')}:\n\n{events_text}")

@bot.message_handler(commands=['semana'])
def show_weekly_events(message):
    chat_id = message.chat.id
    start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + datetime.timedelta(days=7)
    events = calend.get_events(start_date, end_date)
    if not events:
        bot.send_message(chat_id, 'No hay eventos programados para esta semana.')
        return

events_text = format_events(events)
bot.send_message(chat_id, f"Eventos para la semana del {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}:\n\n{events_text}")

@bot.message_handler(commands=['dia'])
def show_daily_events(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Introduce la fecha en formato YYYY-MM-DD:')
    bot.register_next_step_handler(msg, show_daily_events_step2)

def show_daily_events_step2(message):
    chat_id = message.chat.id
    try:
        date = datetime.datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(chat_id, 'Fecha inválida. Introduce la fecha en formato YYYY-MM-DD.')
        bot.register_next_step_handler(message, show_daily_events_step2)
        return

events = calend.get_events(date, date)
if not events:
    bot.send_message(chat_id, f"No hay eventos programados para el día {date.strftime('%d/%m/%Y')}")
else:
    for event in events:
        text = f"{event.name}\n"
        if event.start_time:
            text += f"Hora de inicio: {event.start_time.strftime('%H:%M')}\n"
        if event.end_time:
            text += f"Hora de fin: {event.end_time.strftime('%H:%M')}\n"
        if event.repeats:
            text += f"Repite cada {event.repeats}\n"
        if event.link:
            text += f"Link: {event.link}\n"
        bot.send_message(chat_id, text)

bot.polling()

