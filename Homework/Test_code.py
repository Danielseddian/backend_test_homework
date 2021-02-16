import datetime as dt

def get_week_stats():
    now = dt.datetime.now()
    day = now - dt.timedelta(days=7)
    while day <= now:
        return(day.date())
        day += dt.timedelta(days=1)
        

print(get_week_stats())


'''import datetime as dt


# Создать класс под объект Record cо свойствами amount, comment, date.
# Если дата не задана явно, указать текущее время.
class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = self.now()
        else:
            self.date = date

    # Задать метод для запроса текущей даты в нужном формате
    def now(self):
        today = dt.datetime.strptime(
            str(dt.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        return dt.datetime.strftime(today, '%d-%m-%Y')


# Создать родительский класс Calculator с пустым списком records и
# паметром limit
class Calculator():
    records = []

    def __init__(self, limit):
        self.limit = limit

    # Добавить метод для пополнения списка новыми записями
    def add_record(self, record):
        self.records.append(record)

    # Добавить метод для суммирования значений amount за определённую дату
    def date_amount(self, what_day):
        total_amount = 0
        for i in self.records:
            if i.date == what_day:
                total_amount += i.amount
        return(total_amount)


# создать дочерний класс CashCalculator со свойствоами limit и carrency
class CashCalculator(Calculator):
    # Добавить константы с курсом валют
    USD_RATE = 74
    EUR_RATE = 90

    # Добавить метод для расчёта остатка на балансе
    def get_today_stats(self):
        today = dt.datetime.strptime(
            str(dt.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        return(super().date_amount(dt.datetime.strftime(today, '%d-%m-%Y')))

    # Добавить метод для конвертации баланса в различные валюты
    def exchange(self, currency):
        balance = abs(self.limit - self.get_today_stats())
        if currency == 'rub':
            exchange = f'{balance} руб'
            return(exchange)
        elif currency == 'eur':
            exchange = f'{round(balance / self.EUR_RATE, 2)} евро'
            return(exchange)
        elif currency == 'usd':
            exchange = f'{round(balance / self.USD_RATE, 2)} долл'
            return(exchange)

    # Добавить метод для оповещения пользователя о балансе
    def get_today_cash_remained(self, currency):
        exchange = self.exchange(currency)
        expenses = self.get_today_stats()
        if (
                currency == 'eur'
                or currency == 'usd'
                or currency == 'rub'):
            if expenses < self.limit:
                return(f'На сегодня осталось {exchange}')
            elif expenses == self.limit:
                return('Денег нет, держись')
            elif expenses > self.limit:
                return(f'Денег нет, держись: твой долг - {exchange}')
        else:
            return(
                f'Прости, я пока не умею считать в {currency}. Лучше'
                'спроси про рубли (rub), евро (eur) или доллары (usd).')

#    def get_week_stats():

# Добавить дочерний класс CaloriesCalculator для Calculator
class CaloriesCalculator(Calculator):

    # Добавить метод для расчёта остатка на балансе
    def get_today_stats(self):
        today = dt.datetime.strptime(
            str(dt.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        return(super().date_amount(dt.datetime.strftime(today, '%d-%m-%Y')))

    def get_calories_remained(self):
        eated = self.get_today_stats()
        balance = self.limit - eated
        if eated < self.limit:
            return(
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {balance} кКал')
        else:
            return('Хватит есть!')

#    def get_week_stats():


# Cоздадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
# Дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# И к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# А тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(
                                  amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))
# Должно напечататься
# На сегодня осталось 555 руб
'''