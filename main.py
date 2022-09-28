from views import WelcomeView

from controllers import TournamentsController, Data

WelcomeView.welcome()

Data.load()
print("")

tournaments_self = TournamentsController()
TournamentsController.main(tournaments_self)
