import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Activer le support des clés étrangères
cursor.execute("PRAGMA foreign_keys = ON;")

# Le script SQL pour créer les tables
sql_script = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    entry_date DATE NOT NULL,
    severity INTEGER CHECK (severity BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE triggers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE reactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE daily_entry_triggers (
    entry_id INTEGER NOT NULL,
    trigger_id INTEGER NOT NULL,
    PRIMARY KEY (entry_id, trigger_id),
    FOREIGN KEY (entry_id) REFERENCES daily_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (trigger_id) REFERENCES triggers(id) ON DELETE CASCADE
);

CREATE TABLE daily_entry_reactions (
    entry_id INTEGER NOT NULL,
    reaction_id INTEGER NOT NULL,
    PRIMARY KEY (entry_id, reaction_id),
    FOREIGN KEY (entry_id) REFERENCES daily_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (reaction_id) REFERENCES reactions(id) ON DELETE CASCADE
);

"""

# Exécution du script SQL
cursor.executescript(sql_script)

# Validation des changements et fermeture de la connexion
conn.commit()
conn.close()