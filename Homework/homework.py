import datetime as dt


# Создать класс под объект Record cо свойствами amount, comment, date.
# Если дата не задана явно, указать текущее время.
class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = self.date_transform(date)

    # Задать метод для запроса текущей даты в нужном формате
    def date_transform(self, date=None):
        if date is None:
            now = dt.datetime.now()
            return(now.date())
        else:
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            return(moment.date())


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

    # Добавить метод для расчёта суммы amount в течение дня
    def get_today_stats(self):
        now = dt.datetime.now()
        return(self.date_amount(now.date()))

    # Добавить метод для расчёта суммы amount в течение недели
    def get_week_stats(self):
        now = dt.datetime.now()
        day = now - dt.timedelta(days=7)
        count = 0
        while day <= now:
            count += self.date_amount(day.date())
            day += dt.timedelta(days=1)
        return(count)


# создать дочерний класс CashCalculator со свойствоами limit и carrency
class CashCalculator(Calculator):
    # Добавить константы с курсом валют
    USD_RATE = 74
    EUR_RATE = 90

    # Добавить метод для расчёта баланса и конвертации в различные валюты
    def exchange(self, currency):
        balance = abs(self.limit - super().get_today_stats())
        if currency == 'eur':
            exchange = round(balance / self.EUR_RATE, 2)
            return(f'{exchange} евро')
        elif currency == 'usd':
            exchange = round(balance / self.USD_RATE, 2)
            return(f'{exchange} долл')
        else:
            return(f'{balance} руб')

    # Добавить метод для оповещения пользователя о балансе
    def get_today_cash_remained(self, currency):
        exchange = self.exchange(currency)
        expenses = super().get_today_stats()
        if (
                currency == 'eur'
                or currency == 'usd'
                or currency == 'rub'):
            if expenses < self.limit:
                return(f'На сегодня осталось {exchange}')
            elif expenses == self.limit:
                return('Денег нет, держись')
            else:
                return(f'Денег нет, держись: твой долг - {exchange}')
        else:
            return(
                f'Прости, я пока не умею считать в {currency}. Лучше '
                'спроси про рубли (rub), евро (eur) или доллары (usd).')


# Добавить дочерний класс CaloriesCalculator для Calculator
class CaloriesCalculator(Calculator):

    # Добавить метод для информирования об оставшихся каллориях
    def get_calories_remained(self):
        eated = super().get_today_stats()
        balance = self.limit - eated
        if eated < self.limit:
            return(
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {balance} кКал')
        else:
            return('Хватит есть!')


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
