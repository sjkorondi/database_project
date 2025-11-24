DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS quests;

CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL UNIQUE,
             password_hash TEXT NOT NULL);

 CREATE TABLE IF NOT EXISTS characters (
                character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                character_name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                class_id TEXT NOT NULL,
                quest_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_name),
                FOREIGN KEY (quest_id) REFERENCES quests(quest_id));

CREATE TABLE IF NOT EXISTS items (
             item_id INTEGER PRIMARY KEY AUTOINCREMENT,
             item_name TEXT NOT NULL,
             item_type TEXT NOT NULL,
             item_weight INTEGER NOT NULL,
             item_value INTEGER NOT NULL);

INSERT INTO items (item_name, item_type, item_weight, item_value) VALUES
('Iron Sword', 'Weapon', 6, 25),
('Wooden Shield', 'Armor', 8, 18),
('Healing Potion', 'Consumable', 1, 50),
('Leather Boots', 'Armor', 3, 12),
('Arcane Spellbook', 'Magic', 4, 120),
('Steel Dagger', 'Weapon', 2, 15),
('Hunter’s Bow', 'Weapon', 3, 40),
('Mystic Amulet', 'Magic', 1, 200),
('Adventurer’s Pack', 'Gear', 10, 30),
('Firebomb', 'Consumable', 1, 60);

CREATE TABLE IF NOT EXISTS inventory (
             character_id INTEGER,
             item_id INTEGER,
             quantity INTEGER DEFAULT 1,
             FOREIGN KEY (character_id) REFERENCES characters(character_id),
             FOREIGN KEY (item_id) REFERENCES items(item_id));

CREATE TABLE IF NOT EXISTS classes (
             class_name TEXT PRIMARY KEY,
             class_ability TEXT NOT NULL);

INSERT INTO classes (class_name, class_ability) VALUES
('Barbarian', 'A fierce warrior fueled by rage, dealing massive melee damage.'),
('Bard', 'A versatile performer who uses music and magic to inspire allies.'),
('Cleric', 'A holy spellcaster with powerful healing and protective abilities.'),
('Druid', 'A nature-bound caster who can shapeshift into beasts.'),
('Fighter', 'A master of weapons and armor with unmatched combat versatility.'),
('Monk', 'A martial artist using ki to perform supernatural techniques.'),
('Paladin', 'A holy knight combining divine magic with melee combat.'),
('Ranger', 'A wilderness scout specializing in ranged attacks and animal companions.'),
('Rogue', 'A stealthy trickster skilled in sneak attacks and traps.'),
('Wizard', 'A scholar of arcane magic with potent offensive spells.');

CREATE TABLE IF NOT EXISTS quests (
             quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
             quest_enemy TEXT NOT NULL,
             quest_reward TEXT NOT NULL);

INSERT INTO quests (quest_enemy, quest_reward) VALUES
('Goblin Chief', '50 gold'),
('Forest Troll', 'Enchanted bow'),
('Undead Knight', '120 gold'),
('Cave Spider Queen', 'Potion bundle'),
('Bandit Captain', 'Steel armor'),
('Fire Drake', 'Rare gemstones'),
('Haunted Spirit', 'Blessed amulet'),
('Ogre Brute', '200 gold'),
('Swamp Lizardlord', 'Poison-resistant cloak'),
('Mountain Giant', 'Chest of coins');