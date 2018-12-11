import json
import sqlite3 as sqlite
DB_NAME = 'league_of_legend.sqlite'

def create_db():
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()
    
    statement = '''
        DROP TABLE IF EXISTS 'Champs_info';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Abilities';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Panel_props';
    '''
    cur.execute(statement)
    conn.commit()

    statement1 = '''
        CREATE TABLE `Champs_info` (
            `Champ_id` INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            `Name` TEXT NOT NULL,
            `Type` TEXT NOT NULL,
            `Region` TEXT NOT NULL,
            `Quote` TEXT NOT NULL,
            `Story_url` TEXT NOT NULL,
            `Champ_url` TEXT NOT NULL
        );
    '''
    cur.execute(statement1)

    statement2 = '''
        CREATE TABLE `Abilities` (
            `Ability_id` INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            `Name` TEXT NOT NULL,
            `Type` TEXT NOT NULL,
            `Cost` TEXT,
            `Range` TEXT, 
            `Desc` TEXT NOT NULL,
            `Champ_id` INTEGER NOT NULL, 
            CONSTRAINT fk_champ
                FOREIGN KEY (Champ_id)
                REFERENCES Champs_info(Champ_id)        
    );
    '''
    cur.execute(statement2)

    statement3 = '''
        CREATE TABLE `Panel_props` (
            `Id` INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            `Health_init` TEXT NOT NULL,
            `Health_incre` TEXT NOT NULL,
            `Att_damage_init` TEXT NOT NULL,
            `Att_damage_incre` TEXT NOT NULL,
            `Att_speed_init` TEXT NOT NULL,
            `Att_speed_incre` TEXT NOT NULL,
            `move_speed` TEXT NOT NULL,
            `health_regen_init` TEXT NOT NULL,
            `health_regen_incre` TEXT NOT NULL,
            `armor_init` TEXT NOT NULL,
            `armor_incre` TEXT NOT NULL,
            `magic_resist_init` TEXT NOT NULL,
            `magic_resist_incre` TEXT NOT NULL,
            `Champ_id` INTEGER NOT NULL, 
            CONSTRAINT fk_champ
                FOREIGN KEY (Champ_id)
                REFERENCES Champs_info(Champ_id)
        );
    '''

    cur.execute(statement3)

    # Close connection
    conn.commit()
    conn.close()

def populate_db():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()
    with open('final_data.json') as f:
        champ_dict = json.loads(f.read())
        for champ in champ_dict:
            # insert into champs_info
            champ_name = champ_dict[champ]['name']
            champ_type = champ_dict[champ]['type']
            champ_region = champ_dict[champ]['region']
            champ_quote = champ_dict[champ]['quote']
            champ_story_url = champ_dict[champ]['story_url']
            champ_url = champ_dict[champ]['url']
            statement = '''
                INSERT INTO `Champs_info` (Name, Type, Region, Quote, Story_url, Champ_url)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            cur.execute(statement, (champ_name, champ_type,
                                    champ_region, champ_quote, champ_story_url, champ_url))
            # get champ_id
            statement = 'SELECT Champ_id FROM Champs_info WHERE Name=?'
            cur.execute(statement, (champ_name,))
            champ_id = cur.fetchone()[0]

            # insert into abilities
            champ_abilities = champ_dict[champ]['abilities']
            statement = '''
                INSERT INTO `Abilities` (Name, Type, Desc, Champ_id)
                VALUES (?, ?, ?, ?)
            '''
            # passive
            ability_name = champ_abilities[0]
            ability_type = 'Passive'
            ability_desc = champ_abilities[1]

            cur.execute(statement, (ability_name,
                                    ability_type, ability_desc, champ_id))
            # active
            statement = '''
                INSERT INTO `Abilities` (Name, Type, Cost, Range, Desc, Champ_id)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            count = 0
            for i in range(2, 14, 3):
                count += 1
                ability_name = champ_abilities[i]
                if count == 1:
                    ability_type = 'Active Q'
                if count == 2:
                    ability_type = 'Active W'
                if count == 3:
                    ability_type = 'Active E'
                if count == 4:
                    ability_type = 'Active R'
                ability_c_r = champ_abilities[i + 1].split("###")
                ability_cost = ability_c_r[0].split(":")[1]
                ability_range = ability_c_r[1].split(':')[1]
                ability_descs = champ_abilities[i + 2].split("###")
                ability_desc = ability_descs[0] + "     " + ability_descs[1]
                cur.execute(statement, (ability_name, ability_type,
                                        ability_cost, ability_range, ability_desc, champ_id))

            # insert into panel_props
            panel_prop = champ_dict[champ]['panel_prop']
            health = panel_prop['health']
            att_damage = panel_prop['att_damage']
            att_speed = panel_prop['att_speed']
            mv_speed = panel_prop['mv_speed']
            hp_regen = panel_prop['hp_regen']
            armor = panel_prop['armor']
            mr = panel_prop['mr']
            statement = '''
                INSERT INTO `Panel_props` (Health_init, Health_incre, Att_damage_init, Att_damage_incre, Att_speed_init, Att_speed_incre, move_speed, health_regen_init, health_regen_incre, armor_init, armor_incre, magic_resist_init, magic_resist_incre, champ_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cur.execute(statement, (health[0], health[1], att_damage[0], att_damage[1], att_speed[0], att_speed[1], mv_speed, hp_regen[0], hp_regen[1], armor[0], armor[1], mr[0], mr[1], champ_id))
    # Close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    populate_db()
