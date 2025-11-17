# file to initialize sqlite3 database

import sqlite3 as sql

conn = sql.connect('project_database.db')
curr = conn.cursor()

curr.execute('''
    CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL UNIQUE,
             password_hash TEXT NOT NULL)''') # needed user table for user authentication

curr.execute('''
    CREATE TABLE IF NOT EXISTS characters (
                character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                character_name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                class_id INTEGER,
                quest_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (quest_id) REFERENCES quests(quest_id))''')

curr.execute('''
    CREATE TABLE IF NOT EXISTS items (
             item_id INTEGER PRIMARY KEY AUTOINCREMENT,
             item_name TEXT NOT NULL,
             item_type TEXT NOT NULL,
             item_weight INTEGER NOT NULL,
             item_value INTEGER NOT NULL)''')

curr.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
             character_id INTEGER,
             item_id INTEGER,
             quantity INTEGER DEFAULT 1,
             FOREIGN KEY (character_id) REFERENCES characters(character_id),
             FOREIGN KEY (item_id) REFERENCES items(item_id))''')

curr.execute('''
    CREATE TABLE IF NOT EXISTS classes (
             class_name TEXT PRIMARY KEY,
             class_ability TEXT NOT NULL)''')

curr.execute('''
    CREATE TABLE IF NOT EXISTS quests (
             quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
             quest_enemy TEXT NOT NULL,
             quest_reward TEXT NOT NULL)''')

conn.commit()
conn.close()