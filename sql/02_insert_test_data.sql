INSERT INTO users (username, email) VALUES
('obelix', 'obelix@example.com'),
('tintin', 'tintin@example.com');

INSERT INTO triggers (name) VALUES
('bruit'),
('promeneur'),
('chien'),
('vélo'),
('visiteur'),
('joggeur'),
('chat'),
('chien-ennemi'),
('enfant'),
('voiture'),
('skate'),
('moto');

INSERT INTO reactions (name) VALUES
('aboiement'),
('tremblement'),
('fuite'),
('grognement'),
('regard fixe'),
('calme');

INSERT INTO daily_entries (user_id, entry_date, severity, comment) VALUES
(1, '2025-04-16', 7, 'Gros aboiement en voyant un vélo'),
(1, '2025-04-17', 4, 'Plus calme aujourd’hui, juste un petit grognement au bruit.'),
(2, '2025-04-17', 5, 'Réaction moyenne à un visiteur à la maison.');

INSERT INTO daily_entry_triggers (entry_id, trigger_id) VALUES
(1, 4), -- vélo
(2, 1), -- bruit
(3, 5); -- visiteur

INSERT INTO daily_entry_reactions (entry_id, reaction_id) VALUES
(1, 1), -- aboiement
(2, 4), -- grognement
(3, 3); -- fuite
