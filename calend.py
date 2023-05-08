import datetime

class Calendar:
    def __init__(self):
        self.events = {}


    def add_event(self, date, time=None, repeat=None, link=None):
        if date not in self.events:
            self.events[date] = []
        self.events[date].append({'time': time, 'repeat': repeat, 'link': link})
        return "Evento añadido exitosamente"

    def set_alarm(self, date, time):
        event_time = datetime.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M')
        current_time = datetime.datetime.now()
        time_diff = (event_time - current_time).total_seconds()
        if time_diff <= 0:
            return "No se puede establecer una alarma en el pasado"
        return "Alarma establecida para " + date + " " + time

    def get_events_by_day(self, date):
        if date not in self.events:
            return "No hay eventos para este día"
        events = self.events[date]
        return self.format_events(events)

    def get_events_by_week(self, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = date_obj - datetime.timedelta(days=date_obj.weekday())
        end_date = start_date + datetime.timedelta(days=6)
        week_events = {}
        for i in range(7):
            day = start_date + datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            if day_str in self.events:
                week_events[day_str] = self.events[day_str]
        return self.format_week_events(start_date, end_date, week_events)

    def get_events_by_month(self, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = date_obj.replace(day=1)
        end_date = (start_date + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        month_events = {}
        for i in range((end_date - start_date).days + 1):
            day = start_date + datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            if day_str in self.events:
                month_events[day_str] = self.events[day_str]
        return self.format_month_events(start_date, end_date, month_events)

    def format_events(self, events):
        event_str = ''
        for i, event in enumerate(events):
            event_str += '\n{}. Hora: {}, Repetición: {}, Link: {}'.format(i + 1, event['time'], event['repeat'], event['link'])
        return event_str

    def format_week_events(self, start_date, end_date, week_events):
        week_str = 'Eventos de {} al {}:'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        for date, events in week_events.items():
            week_str += '\n\n{}:{}'.format(date, self.format_events(events))
        return week_str

    def format_month_events(self, start_date, end_date, month_events):
        month_str = 'Eventos de {} al {}:'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        for date, events in month_events.items():
            month_str += '\n\n{}:{}'.format(date, self.format_events(events))
        return month_str
