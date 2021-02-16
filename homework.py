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
        self.today = dt.date.today()

    def add_record(self, record):
        self.records.append(record)

    # Метод для расчёта суммы amount в течение дня
    def get_today_stats(self):
        return sum(record.amount for record in self.records
                   if record.date == self.today)

    # Метод для расчёта суммы amount в течение недели
    def get_week_stats(self):
        return sum(record.amount for record in self.records
                   if record.date > self.today - self.WEEK_AGO
                   and record.date <= self.today)


class CashCalculator(Calculator):
    EURO_RATE = 70.00
    USD_RATE = 60.00
    RUB_RATE = 1
    CURRENCYS = {'rub': [RUB_RATE, 'руб'], 'eur': [EURO_RATE, 'Euro'],
                 'usd': [USD_RATE, 'USD']}
    ERROR_WARNING = 'Не удаётся посчитать в {currency}'
    POS_BALANCE = 'На сегодня осталось {balance} {string_currency}'
    ZERO_BALANCE = 'Денег нет, держись'
    NEG_BALANCE = 'Денег нет, держись: твой долг - {balance} {string_currency}'

    # Оповещение пользователя об остатке денежных средств
    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCYS:
            raise ValueError(self.ERROR_WARNING.format(currency=currency))
        balance = self.limit - self.get_today_stats()
        if balance == 0:
            return self.ZERO_BALANCE
        exchange = round(balance / self.CURRENCYS[currency][0], 2)
        string_currency = self.CURRENCYS[currency][1]
        if balance > 0:
            return self.POS_BALANCE.format(balance=exchange,
                                           string_currency=string_currency)
        return self.NEG_BALANCE.format(balance=abs(exchange),
                                       string_currency=string_currency)


class CaloriesCalculator(Calculator):
    LOW_CALORIIES = ('Сегодня можно съесть что-нибудь ещё, но с общей'
                     ' калорийностью не более {balance} кКал')
    LOT_CALORIES = 'Хватит есть!'

    # Оповещение пользователя о каллориях за день
    def get_calories_remained(self):
        balance = self.limit - self.get_today_stats()
        if balance > 0:
            return self.LOW_CALORIES.format(balance=balance)
        return self.LOT_CALORIES


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
