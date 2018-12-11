from data_access import *
from data_storage import *
from leagueOfLegend import *
import unittest

class TestDataAccess(unittest.TestCase):
    def test_cache(self):
        base_url = 'https://universe.leagueoflegends.com'
        extended_url = '/en_US/champions/'
        url = base_url + extended_url
        try:
            cache_file = open(CACHE_FNAME, 'r')
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents)
            cache_file.close()
            html = CACHE_DICTION[url]
            page = BeautifulSoup(html, 'html.parser')
            champ_dict = {}
            champs = page.find_all(class_='ChampionsList__item__30l')
            for champ in champs:
                champ_url = champ.find('a')['href']
                champ_name = champ.find('h1').text
                champ_key = re.sub("[^A-Za-z]", "", champ_name).lower()
                champ_dict[champ_key] = {}
                champ_dict[champ_key]['url'] = base_url + champ_url
                champ_dict[champ_key]['name'] = champ_name
        except:
            self.fail()
            
    def test_get_champ_dictionary(self):
        base_url = 'https://universe.leagueoflegends.com'
        extended_url = '/en_US/champions/'
        champ_dict = get_champ_list(base_url, extended_url)
        self.assertEqual(len(champ_dict), 142)
        aatrox_url = 'https://na.leagueoflegends.com/en/game-info/champions/Aatrox/'
        aatrox_story_url = 'https://universe.leagueoflegends.com/en_US/story/champion/aatrox/'
        yasuo_url = 'https://na.leagueoflegends.com/en/game-info/champions/Yasuo/'
        yasuo_story_url = 'https://universe.leagueoflegends.com/en_US/story/champion/yasuo/'

        get_game_info_url(champ_dict)
        self.assertEqual(champ_dict['aatrox']['game_info_url'], aatrox_url)
        self.assertEqual(champ_dict['yasuo']['game_info_url'], yasuo_url)
        for champ_key in champ_dict:
            champ_url = champ_dict[champ_key]['url']
            get_champ_background(champ_dict, champ_url, champ_key)
            game_info_url = champ_dict[champ_key]['game_info_url']
            get_champ_game_info(champ_dict, game_info_url, champ_key)
        self.assertEqual(champ_dict['aatrox']['story_url'], aatrox_story_url)
        self.assertEqual(champ_dict['yasuo']['story_url'], yasuo_story_url)
        self.assertEqual(champ_dict['aatrox']
                         ['panel_prop']['health'][0], '580')
        self.assertEqual(champ_dict['aatrox']['panel_prop']['health'][1], '80')
        self.assertEqual(champ_dict['yasuo']['panel_prop']['health'][0], '523')
        self.assertEqual(champ_dict['yasuo']['panel_prop']['health'][1], '87')
        self.assertEqual(champ_dict['aatrox']
                          ['abilities'][0], "Deathbringer Stance")
        self.assertEqual(champ_dict['aatrox']
                          ['abilities'][2], "The Darkin Blade")
        self.assertEqual(champ_dict['yasuo']
                          ['abilities'][0], "Way of the Wanderer")
        self.assertEqual(champ_dict['yasuo']['abilities'][2], "Steel Tempest")


class TestDataStorage(unittest.TestCase):
    # check Champs_info table   
    def test_champ_info_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        stat = 'SELECT Name FROM Champs_info'
        cur.execute(stat)
        results = cur.fetchall()
        self.assertIn(("Aatrox",), results)
        self.assertEqual(len(results), 141)
        conn.close()

    # check Abilities table
    def test_skills_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        stat = 'SELECT Name FROM Abilities WHERE Champ_id=1'
        cur.execute(stat)
        results = cur.fetchall()
        self.assertEqual(len(results), 5)
        self.assertIn(("The Darkin Blade",),results)
        conn.close()
    # check Panel_props table
    def test_panel_prop_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()
        stat = 'SELECT Health_init, move_speed FROM Panel_props WHERE Champ_id=1'
        cur.execute(stat)
        results = cur.fetchone()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], '580')
        self.assertEqual(results[1], '345')
        conn.close()

class TestProcess(unittest.TestCase):
    def test_champ_class(self):
        panel_props = {'health': 500,
            'health_incre':10,
            'att_damage':20,
            'att_damage_incre': 2,
            'att_speed':0,
            'att_speed_incre':0.15,
            'mv_speed':345,
            'health_regen':0.21,
            'health_regen_incre':0.01,
            'armor':30,
            'armor_incre':2,
            'mr':20,
            'mr_incre':1
        }
        champ = Champ(name="BigHuang", _type="Fighter", region="KKK", quote="No body can survive", panel_props=panel_props)
        self.assertEqual(champ.name, "BigHuang")
        self.assertEqual(champ.health, 500)
        self.assertEqual(champ._type, "Fighter")
        self.assertEqual(champ.mr, 20)
        self.assertEqual(len(champ.get_level_props()), 7)
        self.assertEqual(champ.get_level_props(11)[0], 600)

    def test_list_and_show(self):
        command = "list types"
        command_list = command.split()
        result = process_normal_command(command_list)
        self.assertEqual(len(result), 6)
        self.assertIn("Fighter", result[0])

        command = "show skills yasuo"
        command_list = command.split()
        result_list = process_normal_command(command_list)
        self.assertEqual(len(result_list), 5)
        self.assertIn("Way of the Wanderer", result_list[0][0])
    
    def test_plot_pie_chart(self):
        data = ["Fighter:39", "Mage:31", "Assassin:16", "Tank:19", "Marksman:22", "Support:14"]
        try:
            plot_pie_chart(data, "for test")
        except:
            self.fail()
    def test_plot_bar_chart(self):
        panel_props = {'health': 500,
            'health_incre':10,
            'att_damage':20,
            'att_damage_incre': 2,
            'att_speed':0,
            'att_speed_incre':0.15,
            'mv_speed':345,
            'health_regen':0.21,
            'health_regen_incre':0.01,
            'armor':30,
            'armor_incre':2,
            'mr':20,
            'mr_incre':1
        }
        champ = Champ(panel_props=panel_props)
        try:
            plot_level_bar_chart(champ)
        except:
            self.fail()
if __name__ == '__main__':
    unittest.main()
