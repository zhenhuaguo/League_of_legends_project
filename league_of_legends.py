import sqlite3 as sqlite
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
DB_NAME = 'league_of_legend.sqlite'

class Champ:
    def __init__(self, name=None, _type=None, region=None, quote=None, abilities=None, panel_props=None):
        self.name = name
        self._type = _type
        self.region = region
        self.quote = quote
        if abilities:
            self.P = abilities[0]
            self.Q = abilities[1]
            self.W = abilities[2]
            self.E = abilities[3]
            self.R = abilities[4]
        self.health = panel_props['health']
        self.att_damage = panel_props['att_damage']
        self.att_speed = panel_props['att_speed']
        self.mv_speed = panel_props['mv_speed']
        self.health_regen = panel_props['health_regen']
        self.armor = panel_props['armor']
        self.mr = panel_props['mr']

        self.health_incre = panel_props['health_incre']
        self.att_damage_incre = panel_props['att_damage_incre']
        self.att_speed_incre = panel_props['att_speed_incre']
        self.health_regen_incre = panel_props['health_regen_incre']
        self.armor_incre = panel_props['armor_incre']
        self.mr_incre = panel_props['mr_incre']

    def get_level_props(self, level=1):
        
        health = float(self.health) + (level - 1) * float(self.health_incre)
        att_damage = float(self.att_damage) + (level - 1) * float(self.att_damage_incre)
        att_speed = float(self.att_speed) + (level - 1) * float(self.att_speed_incre)
        health_regen = float(self.health_regen) + (level - 1) * float(self.health_regen_incre)
        armor = float(self.armor) + (level - 1) * float(self.armor_incre)
        mr = float(self.mr) + (level - 1) * float(self.mr_incre)
        prop = [health, att_damage, att_speed, self.mv_speed,health_regen, armor, mr]
        return prop


# Implement logic to process user commands
def load_help_text():
    with open('help.txt') as f:
        return f.read()

def process_normal_command(command_list):
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()
    result_list = []
    bad_command = False

    if command_list[0] == 'list':
        if command_list[1] == 'regions':
            try:
                statement = "SELECT DISTINCT Region FROM Champs_info"
                cur.execute(statement)
                region_list = cur.fetchall()
                num_list = []
                for region in region_list:
                    statement = "SELECT COUNT (Region) FROM Champs_info WHERE Region='" + region[0] + "'"
                    cur.execute(statement)
                    res = cur.fetchone()[0]
                    num_list.append(res)
                for i in range(len(region_list)):
                    item = region_list[i][0] + ": " + str(num_list[i])
                    result_list.append(item)
            except:
                print("Make sure you type the right parameter")
                result_list = []
        elif command_list[1] == 'types':
            try:
                statement = "SELECT DISTINCT Type From Champs_info"
                cur.execute(statement)
                type_list = cur.fetchall()
                num_list = []
                for _type in type_list:
                    statement = "SELECT COUNT (Type) FROM Champs_info WHERE Type='" + _type[0] + "'"
                    cur.execute(statement)
                    res = cur.fetchone()[0]
                    num_list.append(res)
                for i in range(len(type_list)):
                    item = type_list[i][0] + ": " + str(num_list[i])
                    result_list.append(item)
            except:
                print("Make sure you type the right parameter")
                result_list = []
        elif command_list[1] == 'champs':
            statement = "SELECT Name FROM Champs_info"
            range_param = " WHERE Name LIKE '%'"
            region_param = " AND Region LIKE '%'"
            type_param = " AND Type LIKE '%'"
            for word in command_list:
                if 'range' in word:
                    a, b = word.split("=")
                    range_param =  " WHERE Name LIKE '{}%'".format(b.title())
                if 'region' in word:
                    a, b = word.split("=")
                    region_param = " AND Region='" + b.title() + "'"
                if 'type' in word:
                    a, b = word.split("=")
                    type_param = " AND Type='" + b.title() + "'"
            statement += range_param
            statement += region_param
            statement += type_param
            try:
                cur.execute(statement)
                result_list = cur.fetchall()
            except:
                print("Make sure you type the right parameter")
                result_list = []
        else:
            bad_command = True
            result_list = []
    
    elif command_list[0] == 'show':
        skip = False
        if len(command_list) == 3:
            statement = "SELECT Champ_id, Name, Type, Region, Quote, Story_url, Champ_url FROM Champs_info WHERE Name='" + command_list[2].title() + "'"    
            try:
                cur.execute(statement)
                result_list = cur.fetchone()
                champ_id = result_list[0]
            except:
                bad_command = True
            
            if not bad_command:
                if command_list[1] == 'champ':
                    skip = True
                elif command_list[1] == 'skills':
                    statement = "SELECT Name, Type, Cost, Range, Desc FROM Abilities WHERE Champ_id=?"
                elif command_list[1] == 'props':
                    statement = '''
                        SELECT Health_init, Health_incre, Att_damage_init, Att_damage_incre, Att_speed_init, Att_speed_incre, move_speed, health_regen_init, 
                        health_regen_incre, armor_init, armor_incre, magic_resist_init, magic_resist_incre 
                        FROM Panel_props
                        WHERE Champ_id=?
                    '''
                else:
                    bad_command = True
        else:
            bad_command = True

        if skip:
            result_list = result_list[1:]   
        elif not bad_command:
            try:
                cur.execute(statement, (champ_id,))
                result_list = cur.fetchall()
            except:
                print("Make sure you type the right name of the champion")
                result_list = []
        else:
            result_list = []
    
    conn.close()
    return result_list
    
def process_compare_command(champ1, champ2):
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()
    try:
        statement1 = "SELECT Champ_id, Name, Type, Region, Quote FROM Champs_info WHERE Name='" + champ1.title() + "'"    
        cur.execute(statement1)
        result_a = cur.fetchone()
        champ_a_id = result_a[0]
        champ_a_name = result_a[1]
        champ_a_type = result_a[2]
        champ_a_region = result_a[3]
        champ_a_quote = result_a[4]
    except:
        print("Make sure you type the right name of the champion")
        conn.close()
        return Champ(), Champ()   
    try:
        statement2 = "SELECT Champ_id, Name, Type, Region, Quote FROM Champs_info WHERE Name='" + champ2.title() + "'"    
        cur.execute(statement2)
        result_b = cur.fetchone()
        champ_b_id = result_b[0]
        champ_b_name = result_b[1]
        champ_b_type = result_b[2]
        champ_b_region = result_b[3]
        champ_b_quote = result_b[4]
    except:
        print("Make sure you type the right name of the champion")
        return Champ(), Champ()   
    
    abilities_a = []
    statement1 = "SELECT Name, Type, Cost, Range, Desc FROM Abilities WHERE type=? AND Champ_id=?"
    cur.execute(statement1, ("Passive", champ_a_id,))
    abilities_a.append(cur.fetchone())
    cur.execute(statement1, ("Active Q", champ_a_id,))
    abilities_a.append(cur.fetchone())
    cur.execute(statement1, ("Active W", champ_a_id,))
    abilities_a.append(cur.fetchone())
    cur.execute(statement1, ("Active E", champ_a_id,))
    abilities_a.append(cur.fetchone())
    cur.execute(statement1, ("Active R", champ_a_id,))
    abilities_a.append(cur.fetchone())

    statement1 = '''
        SELECT Health_init, Health_incre, Att_damage_init, Att_damage_incre, Att_speed_init, Att_speed_incre, move_speed, health_regen_init, 
        health_regen_incre, armor_init, armor_incre, magic_resist_init, magic_resist_incre 
        FROM Panel_props
        WHERE Champ_id=?
    '''
    cur.execute(statement1, (champ_a_id,))
    props = cur.fetchone()
    panel_props = {'health': props[0],
                    'health_incre':props[1],
                    'att_damage':props[2],
                    'att_damage_incre':props[3],
                    'att_speed':props[4],
                    'att_speed_incre':props[5],
                    'mv_speed':props[6],
                    'health_regen':props[7],
                    'health_regen_incre':props[8],
                    'armor':props[9],
                    'armor_incre':props[10],
                    'mr':props[11],
                    'mr_incre':props[12]
    }
    champ_a = Champ(champ_a_name, champ_a_type, champ_a_region, champ_a_quote, abilities_a, panel_props)
    
    abilities_b = []
    statement2 = "SELECT Name, Type, Cost, Range, Desc FROM Abilities WHERE type=? AND Champ_id=?"
    cur.execute(statement2, ("Passive", champ_b_id,))
    abilities_b.append(cur.fetchone())
    cur.execute(statement2, ("Active Q", champ_b_id,))
    abilities_b.append(cur.fetchone())
    cur.execute(statement2, ("Active W", champ_b_id,))
    abilities_b.append(cur.fetchone())
    cur.execute(statement2, ("Active E", champ_b_id,))
    abilities_b.append(cur.fetchone())
    cur.execute(statement2, ("Active R", champ_b_id,))
    abilities_b.append(cur.fetchone())

    statement2 = '''
        SELECT Health_init, Health_incre, Att_damage_init, Att_damage_incre, Att_speed_init, Att_speed_incre, move_speed, health_regen_init, 
        health_regen_incre, armor_init, armor_incre, magic_resist_init, magic_resist_incre 
        FROM Panel_props
        WHERE Champ_id=?
    '''
    cur.execute(statement2, (champ_b_id,))
    props = cur.fetchone()
    panel_props = {'health': props[0],
                    'health_incre':props[1],
                    'att_damage':props[2],
                    'att_damage_incre':props[3],
                    'att_speed':props[4],
                    'att_speed_incre':props[5],
                    'mv_speed':props[6],
                    'health_regen':props[7],
                    'health_regen_incre':props[8],
                    'armor':props[9],
                    'armor_incre':props[10],
                    'mr':props[11],
                    'mr_incre':props[12]
    }
    champ_b = Champ(champ_b_name, champ_b_type, champ_b_region, champ_b_quote, abilities_b, panel_props)
    conn.close()
    return champ_a, champ_b



def plot_bar_chart(champ_a, champ_b, level):
    champ_a_name = champ_a.name
    champ_b_name = champ_b.name
    xlist=['Health', 'Attack Damage', 'Attack Speed', 'Movement Speed', 'Health Regen', 'Armor', 'Magic Resisit']
    alist = champ_a.get_level_props(level)
    blist = champ_b.get_level_props(level)
    trace1 = go.Bar(
        x=xlist,
        y=alist,
        name=champ_a_name
    )
    trace2 = go.Bar(
        x=xlist,
        y=blist,
        name=champ_b_name
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='grouped-bar')

def plot_level_bar_chart(champ):
    champ_name = champ.name
    xlist=['Health', 'Attack Damage', 'Attack Speed', 'Movement Speed', 'Health Regen', 'Armor', 'Magic Resisit']
    alist = [champ.health, champ.att_damage, champ.att_speed, champ.mv_speed, champ.health_regen, champ.armor, champ.mr]
    blist = [champ.health_incre, champ.att_damage_incre, champ.att_speed_incre, 0, champ.health_regen_incre, champ.armor_incre, champ.mr_incre]
    trace1 = go.Bar(
        x=xlist,
        y=alist,
        name="level 1"
    )
    trace2 = go.Bar(
        x=xlist,
        y=blist,
        name="increment per level"
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='stacked-bar')

def plot_pie_chart(data, plot_name):
    labels = []
    values = []
    for item in data:
        label, value = item.split(":")
        labels.append(label)
        values.append(int(value))

    trace = go.Pie(labels=labels, values=values, name=plot_name)
    py.plot([trace], filename='basic_pie_chart')

def interactive_prompt():
    help_text = load_help_text()
    command = ""
    while command != 'exit':
        command = input("Enter a command or 'exit' to quit: ")
        command = command.lower()
        command_list = command.split()
        if command == 'help':
            print(help_text)
            print("\n")
        elif 'compare' in command:
            level = 1
            if len(command_list) == 3:
                champ1 = command_list[1]
                champ2 = command_list[2]
                champ_a, champ_b = process_compare_command(champ1, champ2)
                print("See the plot to compare the differences")
                plot_bar_chart(champ_a, champ_b, level)
            elif len(command_list) == 4:
                for word in command_list:
                    if 'level' in word:
                        _, level = word.split('=')
                champ1 = command_list[1]
                champ2 = command_list[2]
                level = int(level)
                champ_a, champ_b = process_compare_command(champ1, champ2)
                print("See the plot to compare the differences")
                plot_bar_chart(champ_a, champ_b, level)
            else:
                print("Please type 'help' to see the instruction")
        elif "list" in command or "show" in command:
            result_list = process_normal_command(command_list) 
            if len(result_list) == 0:
                print("Nothing found based on your search")
                print("Please type 'help' to see the instruction or change the command")    
            else:
                if "regions" in command:
                    print("Below are all the regions in League of Legends:")
                    for res in result_list:
                        print(res)
                    show_plot = input("Do you want to see the plot? (y/n)")
                    if "y" in show_plot:
                        plot_pie_chart(result_list, "Champion regions distribution")
                elif "types" in command:
                    print("Below are all the types of champions in League of Legends:")
                    for res in result_list:
                        print(res)
                    show_plot = input("Do you want to see the plot? (y/n)")
                    if "y" in show_plot:
                        plot_pie_chart(result_list, "Champion types distribution")
                elif "champs" in command:
                    print("Champions in League of Legends based on your search:")
                    for res in result_list:
                        print(res[0])
                elif "champ" in command:
                    print("Below are details of the champion you searched:")
                    title = ["Name", "Type", "Region", "Quote", "Story_url", "Champ_url"]
                    for i in range(len(result_list)):
                        print(title[i] + ": " + result_list[i])
                elif "skills" in command:
                    print("Below are skills the champion have:")
                    s = [" %-20s ", '   '," %-20s ", '   '," %-20s ", '   '," %-20s ", '   '," %-50s ", '   ']
                    print(''.join(s) %("Skill Name", "Type", "Cost", "Range", "Description"))
                    for i in result_list:
                        count = 0
                        for j in i:
                            if len(str(i)) > 20:
                                s[2*count - 1] = '...'
                        if i[2] == None:
                            print(''.join(s) % (i[0][:20], i[1][:20], "N/A",  "N/A", i[4][:50]))
                        else:
                            print(''.join(s) % (i[0][:20], i[1][:20], i[2][:20], i[3][:20], i[4][:50]))
                elif "props" in command:
                    print("Below are panel properties of the champion:")
                    title = ["Health_init", "Health_incre", "Att_damage_init", "Att_damage_incre", "Att_speed_init", "Att_speed_incre", "Move_speed", "Health_regen_init", "Health_regen_incre", "Armor_init", "Armor_incre", "Magic_resist_init", "Magic_resist_incre"]
                    for i in range(len(result_list[0])):
                        print(title[i] + ": " + result_list[0][i])
                    show_plot = input("Do you want to see the plot? (y/n)")
                    if "y" in show_plot:
                        panel_props = {'health': result_list[0][0],
                            'health_incre':result_list[0][1],
                            'att_damage':result_list[0][2],
                            'att_damage_incre':result_list[0][3],
                            'att_speed':result_list[0][4],
                            'att_speed_incre':result_list[0][5],
                            'mv_speed':result_list[0][6],
                            'health_regen':result_list[0][7],
                            'health_regen_incre':result_list[0][8],
                            'armor':result_list[0][9],
                            'armor_incre':result_list[0][10],
                            'mr':result_list[0][11],
                            'mr_incre':result_list[0][12]
                        }
                        champ = Champ(panel_props=panel_props)

                        plot_level_bar_chart(champ)
                print('\n')
        elif command == 'exit':
            print("Bye~")
        else:
            print("Command not recognized: ", command) 
            print("Please type 'help' to see the instruction")
            

if __name__=="__main__":
    interactive_prompt()

    
