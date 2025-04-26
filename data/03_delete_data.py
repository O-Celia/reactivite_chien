import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Activer les clés étrangères
cursor.execute("PRAGMA foreign_keys = ON;")

# Supprimer les données
delete_script = """
DELETE FROM daily_entry_reactions;
DELETE FROM daily_entry_triggers;
DELETE FROM daily_entries;
DELETE FROM reactions;
DELETE FROM triggers;
DELETE FROM users;

DELETE FROM sqlite_sequence WHERE name='daily_entry_reactions';
DELETE FROM sqlite_sequence WHERE name='daily_entry_triggers';
DELETE FROM sqlite_sequence WHERE name='daily_entries';
DELETE FROM sqlite_sequence WHERE name='reactions';
DELETE FROM sqlite_sequence WHERE name='triggers';
DELETE FROM sqlite_sequence WHERE name='users';
"""

cursor.executescript(delete_script)
conn.commit()
conn.close()
