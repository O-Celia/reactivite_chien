from database import Base, engine
import models
import os

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'), exist_ok=True)

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("La base de données a été initialisée.")

if __name__ == "__main__":
    init_db()
