import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = (dt.date.today() if date is None else
                     dt.datetime.strptime(date, self.DATE_FORMAT).date())


class Calculator():
    WEEK_AGO = dt.timedelta(days=7)

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
        today = dt.date.today()
        last_week = today - self.WEEK_AGO
        return sum(record.amount for record in self.records
                   if last_week < record.date <= today)


class CashCalculator(Calculator):
    EURO_RATE = 70.00
    USD_RATE = 60.00
    RUB_RATE = 1
    CURRENCYS = {'rub': [RUB_RATE, 'руб'],
                 'eur': [EURO_RATE, 'Euro'],
                 'usd': [USD_RATE, 'USD']}
    ERROR_WARNING = 'Не удаётся посчитать в {show_currency}'
    POSITIV = 'На сегодня осталось {balance} {show_currency}'
    ZERO = 'Денег нет, держись'
    NEGATIV = 'Денег нет, держись: твой долг - {balance} {show_currency}'

    # Оповещение пользователя об остатке денежных средств
    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCYS:
            raise ValueError(self.ERROR_WARNING.format(currency=currency))
        balance = self.limit - self.get_today_stats()
        if balance == 0:
            return self.ZERO
        change, show_currency = self.CURRENCYS[currency]
        exchange = round(balance / change, 2)
        if balance > 0:
            return self.POSITIV.format(balance=exchange,
                                       show_currency=show_currency)
        return self.NEGATIV.format(balance=abs(exchange),
                                   show_currency=show_currency)


class CaloriesCalculator(Calculator):
    TOO_LOW = ('Сегодня можно съесть что-нибудь ещё, но с общей'
               ' калорийностью не более {balance} кКал')
    A_LOT_OF = 'Хватит есть!'

    # Оповещение пользователя о каллориях за день
    def get_calories_remained(self):
        balance = self.limit - self.get_today_stats()
        if balance > 0:
            return self.TOO_LOW.format(balance=balance)
        return self.A_LOT_OF


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
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
    # Должно напечататься
    # На сегодня осталось 555 руб
