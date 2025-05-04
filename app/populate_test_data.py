from database import SessionLocal
from models.user import User
from models.trigger import Trigger
from models.reaction import Reaction

def populate_data():
    db = SessionLocal()

    triggers = [
        "bruit", "promeneur", "chien", "vélo", "visiteur", "joggeur", "chat", "chien-ennemi", "enfant", "voiture", "skate", "moto", "foule", "tonnerre"
    ]

    reactions = [
        "aboiement", "tremblement", "fuite", "grognement", "regard fixe", "queue basse", "morsure", "pincement"
    ]

    for name in triggers:
        db.add(Trigger(name=name))

    for name in reactions:
        db.add(Reaction(name=name))

    db.commit()
    db.close()
    print("Les données de test ont été insérées avec succès.")

if __name__ == "__main__":
    populate_data()
