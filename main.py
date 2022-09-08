from views import welcome_view

from controllers import tournaments_controller, load_data

welcome_view()

load_data()
print("")
tournaments_controller()
