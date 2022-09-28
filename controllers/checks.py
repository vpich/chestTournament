from datetime import datetime
from views import ErrorsViews, ChecksViews


class Check:

    @staticmethod
    def int_input(user_input):
        if user_input.isdigit():
            return True
        else:
            ErrorsViews.unknown_choice()
            ErrorsViews.number_required()
            return False

    @staticmethod
    def date_format(user_input):
        try:
            date_to_check = datetime.strptime(user_input, "%d/%m/%Y")
            return datetime.date(date_to_check)
        except ValueError:
            ErrorsViews.wrong_date_format()
            return False

    @staticmethod
    def deletion():
        choice = ChecksViews.deletion()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            ErrorsViews.unknown_choice()
            Check.deletion()
