CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    entry_date DATE NOT NULL,
    severity INT CHECK (severity BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE triggers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE daily_entry_triggers (
    entry_id INT NOT NULL,
    trigger_id INT NOT NULL,
    PRIMARY KEY (entry_id, trigger_id),
    FOREIGN KEY (entry_id) REFERENCES daily_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (trigger_id) REFERENCES triggers(id) ON DELETE CASCADE
);

CREATE TABLE daily_entry_reactions (
    entry_id INT NOT NULL,
    reaction_id INT NOT NULL,
    PRIMARY KEY (entry_id, reaction_id),
    FOREIGN KEY (entry_id) REFERENCES daily_entries(id) ON DELETE CASCADE,
    FOREIGN KEY (reaction_id) REFERENCES reactions(id) ON DELETE CASCADE
);
