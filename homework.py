import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = self.date_transform(date)

    def date_transform(self, date=None):
        if date is None:
            return dt.date.today()
        return dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator():
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # Метод для расчёта суммы amount в течение дня
    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    # Метод для расчёта суммы amount в течение недели
    def get_week_stats(self):
        week = [dt.date.today() - dt.timedelta(days=day)
                for day in range(7)]
        return sum(record.amount for record in self.records
                   if record.date in week)


class CashCalculator(Calculator):
    EURO_RATE = 70.00
    USD_RATE = 60.00
    RUB_RATE = 1
    EXCHANGE = {'rub': RUB_RATE, 'eur': EURO_RATE, 'usd': USD_RATE}
    CURRENCY = {'rub': 'руб', 'eur': 'Euro', 'usd': 'USD'}
    ANSWER_0 = 'Не удаётся посчитать в {currency}'
    ANSWER_1 = 'На сегодня осталось {balance} {string_currency}'
    ANSWER_2 = 'Денег нет, держись'
    ANSWER_3 = 'Денег нет, держись: твой долг - {balance} {string_currency}'

    # Оповещение пользователя об остатке денежных средств
    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCY:
            raise ValueError(self.ANSWER_0.format(currency=currency))
        balance = self.limit - self.get_today_stats()
        exchange = round(balance / self.EXCHANGE[currency], 2)
        string_currency = self.CURRENCY[currency]
        if balance > 0:
            return self.ANSWER_1.format(balance=exchange,
                                        string_currency=string_currency)
        elif balance == 0:
            return self.ANSWER_2
        return self.ANSWER_3.format(balance=abs(exchange),
                                    string_currency=string_currency)


class CaloriesCalculator(Calculator):
    ANSWER_1 = ('Сегодня можно съесть что-нибудь ещё, но с общей калорийностью'
                ' не более {balance} кКал')
    ANSWER_2 = 'Хватит есть!'

    # Оповещение пользователя о каллориях за день
    def get_calories_remained(self):
        balance = self.limit - self.get_today_stats()
        if balance > 0:
            return self.ANSWER_1.format(balance=balance)
        return self.ANSWER_2


if __name__ == '__main__':
    # Cоздадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)
    # Дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # И к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # А тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='15.02.2021'))
    print(cash_calculator.get_today_cash_remained('rub'))
    # Должно напечататься
    # На сегодня осталось 555 руб
