from .checks import Check
from views import TimeControlView, ErrorsViews


class TimeControl:
    def selection(self):
        time_control_choices = ["Bullet", "Blitz", "Coup rapide"]
        user_choice = TimeControlView.main(time_control_choices)

        if not Check.int_input(user_choice):
            return self.selection()
        else:
            user_choice = int(user_choice)
            if user_choice > 3:
                ErrorsViews.unknown_choice()
                return self.selection()
            elif user_choice == 1:
                return time_control_choices[0]
            elif user_choice == 2:
                return time_control_choices[1]
            elif user_choice == 3:
                return time_control_choices[2]
            else:
                ErrorsViews.unknown_choice()
                ErrorsViews.number_required()
                return self.selection()
