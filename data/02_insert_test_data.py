import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Activer le support des clés étrangères
cursor.execute("PRAGMA foreign_keys = ON;")

# Insérer des utilisateurs dans la table users
cursor.executemany("""
INSERT INTO users (username, email) VALUES (?, ?)
""", [
    ('obelix', 'obelix@example.com'),
    ('tintin', 'tintin@example.com')
])

# Insérer des triggers dans la table triggers
cursor.executemany("""
INSERT INTO triggers (name) VALUES (?)
""", [
    ('bruit',),
    ('promeneur',),
    ('chien',),
    ('vélo',),
    ('visiteur',),
    ('joggeur',),
    ('chat',),
    ('chien-ennemi',),
    ('enfant',),
    ('voiture',),
    ('skate',),
    ('moto',)
])


# Insérer des reactions dans la table reactions
cursor.executemany("""
INSERT INTO reactions (name) VALUES (?)
""", [
    ('aboiement',),
    ('tremblement',),
    ('fuite',),
    ('grognement',),
    ('regard fixe',),
    ('calme',)
])


# Insérer des entrées journalières dans la table daily_entries
cursor.executemany("""
INSERT INTO daily_entries (user_id, entry_date, severity, comment) VALUES (?, ?, ?, ?)
""", [
    (1, '2025-04-16', 5, 'Gros aboiement en voyant un vélo'),
    (1, '2025-04-17', 1, 'Plus calme aujourd’hui, juste un petit grognement au bruit.'),
    (2, '2025-04-17', 3, 'Réaction moyenne à un visiteur à la maison.')
])

# Insérer des relations daily_entry_triggers dans la table daily_entry_triggers
cursor.executemany("""
INSERT INTO daily_entry_triggers (entry_id, trigger_id) VALUES (?, ?)
""", [
    (1, 4),  # vélo
    (2, 1),  # bruit
    (3, 5)   # visiteur
])

# Insérer des relations daily_entry_reactions dans la table daily_entry_reactions
cursor.executemany("""
INSERT INTO daily_entry_reactions (entry_id, reaction_id) VALUES (?, ?)
""", [
    (1, 1),  # aboiement
    (2, 4),  # grognement
    (3, 3)   # fuite
])

# Valider les changements et fermer la connexion
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans la base de données SQLite.")
