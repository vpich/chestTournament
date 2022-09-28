class CrudViews:
    @staticmethod
    def save():
        print("Enregistrement dans le fichier db.json terminé.")

    @staticmethod
    def delete():
        print("Suppression de tous les tournois du fichier db.json terminée")

    @staticmethod
    def cancel_delete():
        print("Suppression annulée")

    @staticmethod
    def file_not_found():
        print("Le fichier db.json est introuvable.")
        print("Aucun chargement de données n'a pu être effectué.")

    @staticmethod
    def load(db_table):
        if not db_table:
            print("Aucune donnée n'a été chargée.")
        else:
            print("Chargement du fichier db.json terminé.")
