DELETE FROM daily_entry_reactions;
DELETE FROM daily_entry_triggers;
DELETE FROM daily_entries;
DELETE FROM reactions;
DELETE FROM triggers;
DELETE FROM users;

ALTER TABLE daily_entry_reactions AUTO_INCREMENT = 1;
ALTER TABLE daily_entry_triggers AUTO_INCREMENT = 1;
ALTER TABLE daily_entries AUTO_INCREMENT = 1;
ALTER TABLE reactions AUTO_INCREMENT = 1;
ALTER TABLE triggers AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;
