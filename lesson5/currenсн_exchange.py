
valid_currencies = ['USD', 'EUR', 'CHF', 'GBP']


class Price:
    def __init__(self, value: int, currency: str) -> None:
        self.value = value
        self.currency = currency

    def convert(self, symbol: str) -> 'Price':
        conversion_rates = {
            'USD': 1.13,
            'EUR': 1.08,
            'CHF': 1,
            'GBP': 0.89
        }

        conversion_rate = conversion_rates.get(self.currency)
        if not conversion_rate:
            raise ValueError(f"Unknown currency: {self.currency}")

        converted_value = self.value * conversion_rate

        if symbol == "CHF":
            return Price(converted_value, "CHF")

        reverse_conversion_rate = conversion_rates.get(symbol)
        if not reverse_conversion_rate:
            raise ValueError(f"Unknown currency: {symbol}")

        final_value = converted_value / reverse_conversion_rate
        return Price(int(final_value), symbol)

    def __add__(self, other: 'Price'):
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only on Price')
        elif self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            converted_self = self.convert(symbol="CHF")
            converted_other = other.convert(symbol="CHF")
            total_value = converted_self.value + converted_other.value
            return Price(total_value, self.currency)

    def __sub__(self, other: 'Price'):
        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            converted_self = self.convert(symbol="CHF")
            converted_other = other.convert(symbol="CHF")
            total_value = converted_self.value - converted_other.value
            return Price(total_value, self.currency)

    def __repr__(self) -> str:
        return f"Price({self.value}, '{self.currency}')"


class Main:
    @staticmethod
    def create_price_object():
        while True:
            try:
                user_in = input('Enter amount and currency. In <<<100 USD>>> format: ')

                if ' ' not in user_in:
                    raise ValueError("The input must contain a space between the amount and the currency.")

                amount, currency = user_in.split(' ')
                currency = currency.strip().upper()

                if currency.strip() not in valid_currencies:
                    raise ValueError(f"Invalid currency. Valid currencies: {', '.join(valid_currencies)}.")

                if not amount.strip().isdigit():
                    raise ValueError("The amount must be a number.")

                price = Price(int(amount), currency.strip())
                return price

            except ValueError as e:
                print(f"Input error: {e}")
                continue

    @staticmethod
    def continue_work():
        while True:
            a = input('Do you wish to continue working? yes/no: ').strip().lower()
            if a == 'no':
                print("Completion of work.")
                return False
            elif a == 'yes':
                return True
            else:
                print("Incorrect input, please try again.")

    @staticmethod
    def run():
        print(f"Available currencies: {', '.join(valid_currencies)}")

        while True:
            g = Main.create_price_object()
            h = Main.create_price_object()

            operator = input('Select an action. <+> or <->: ').strip()
            if operator == '+':
                print(g + h)
            elif operator == '-':
                print(g - h)
            else:
                print(f"Invalid action. Please select <+> or <->. {operator} is not supported.")

            if not Main.continue_work():
                break


if __name__ == '__main__':
    Main.run()
