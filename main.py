from views import WelcomeView, Utilitaries

from controllers import TournamentsController, Data

WelcomeView.welcome()

Data.load()
Utilitaries.empty_space()

tournaments_self = TournamentsController()
TournamentsController.main(tournaments_self)
