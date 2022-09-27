from views import WelcomeView

from controllers import TournamentsController, Data

WelcomeView.welcome()

Data.load()
print("")
TournamentsController.main()
