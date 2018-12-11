import requests
import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import time
import re

######################### start of the cache function  #############################

CACHE_FNAME = 'leagueOfLegend_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


def get_unique_key(url):
    return url


def make_champ_list_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        # Make the request and cache the new data
        browser.get(url)
        html = browser.page_source
        CACHE_DICTION[unique_ident] = html
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def make_champ_background_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        # Make the request and cache the new data
        browser.get(url)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        time.sleep(2)
        browser.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        html = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ChampionDetailGrid__container__1Ic'))).get_attribute('innerHTML')
        CACHE_DICTION[unique_ident] = html
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def make_champ_url_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        # Make the request and cache the new data
        browser.get(url)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        time.sleep(1)
        browser.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        html = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'champion-grid'))).get_attribute('innerHTML')
        CACHE_DICTION[unique_ident] = html
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def make_game_info_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        # Make the request and cache the new data
        browser.get(url)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        time.sleep(2)
        browser.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        browser.execute_script(
            'window.scrollTo(0, 0.5*document.body.scrollHeight);')
        section = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'section-wrapper-content-wrapper')))
        CACHE_DICTION[unique_ident] = [section[0].get_attribute(
            'innerHTML'), section[1].get_attribute('innerHTML')]

        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

######################### end of the cache function  #############################


######################### start of the function to fetch champ info  #############################

def get_champ_list(base_url, extended_url):
    html = make_champ_list_request_using_cache(base_url + extended_url)
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
    return champ_dict


def get_champ_background(champ_dict, url, champ_key):
    html = make_champ_background_request_using_cache(url)
    page = BeautifulSoup(html, 'html.parser')
    champ_quote = page.find('li', 'ChampionQuotes__quote__250').find('p').text
    champ_story = page.find('div', 'ChampionQuotes__biographyText__3-t ').text
    champ_story_url = page.find(
        'li', 'ChampionQuotes__biography__3YI').find('a')['href']
    champ_type = page.find(
        'div', 'PlayerType__typeDescription__ixW').find('h6').text
    champ_region = page.find('div', 'PlayerFaction__factionText__EnR').find(
        'h6').find('span').text
    champ_dict[champ_key]['quote'] = champ_quote
    champ_dict[champ_key]['story'] = champ_story
    champ_dict[champ_key]['type'] = champ_type
    champ_dict[champ_key]['region'] = champ_region
    base_url = 'https://universe.leagueoflegends.com'
    champ_dict[champ_key]['story_url'] = base_url + champ_story_url


def get_game_info_url(champ_dict):
    url = 'https://na.leagueoflegends.com/en/game-info/champions/'
    html = make_champ_url_request_using_cache(url)
    page = BeautifulSoup(html, 'html.parser')
    champ_list = page.find_all('li')
    for champ in champ_list:
        champ_a = champ.find(class_='champ-name').find('a')
        name = champ_a.text
        champ_key = re.sub("[^A-Za-z]", "", name).lower()
        game_url = champ_a['href']
        champ_dict[champ_key]['game_info_url'] = url + game_url


def get_champ_game_info(champ_dict, url, champ_key):
    section = make_game_info_request_using_cache(url)
    top = section[0]
    bottom = section[1]
    # panel properties
    champ_dict[champ_key]['panel_prop'] = {}
    page_top = BeautifulSoup(top, 'html.parser')
    panel_properties = page_top.find_all('span', 'dd-auto-set')
    init_health = panel_properties[1].text
    health_incre = panel_properties[2].text
    champ_dict[champ_key]['panel_prop']['health'] = list(
        (init_health, health_incre))

    init_attack = panel_properties[3].text
    attack_incre = panel_properties[4].text
    champ_dict[champ_key]['panel_prop']['att_damage'] = list(
        (init_attack, attack_incre))

    init_attack_speed = panel_properties[5].text
    attack_speed_incre = panel_properties[6].text
    champ_dict[champ_key]['panel_prop']['att_speed'] = list(
        (init_attack_speed, attack_speed_incre))

    init_move_speed = panel_properties[7].text
    champ_dict[champ_key]['panel_prop']['mv_speed'] = init_move_speed

    init_health_regen = panel_properties[8].text
    health_regen_incre = panel_properties[9].text
    champ_dict[champ_key]['panel_prop']['hp_regen'] = list(
        (init_health_regen, health_regen_incre))

    init_armor = panel_properties[10].text
    armor_incre = panel_properties[11].text
    champ_dict[champ_key]['panel_prop']['armor'] = list(
        (init_armor, armor_incre))

    init_mr = panel_properties[12].text
    mr_incre = panel_properties[13].text
    champ_dict[champ_key]['panel_prop']['mr'] = list((init_mr, mr_incre))
    # abilities

    page_bottom = BeautifulSoup(bottom, 'html.parser')
    alist = []

    p_name = page_bottom.find(id='PName').find('h3').text
    p_desc = page_bottom.find(id='PName').next_sibling.find('p').text
    alist.append(p_name)
    alist.append(p_desc)

    q_name = page_bottom.find(id='QName').find('h3').text
    q_descs = page_bottom.find(id='QName').find('p')
    q_texts = page_bottom.find(id='QName').next_sibling.find_all('p')
    q_descs_span = q_descs.find_all('span')
    q_descs_b = q_descs.find_all('b')
    q_desc = q_descs_b[0].text + q_descs_span[0].text + \
        "###" + q_descs_b[1].text + q_descs_span[1].text

    q_text = ""
    for text in q_texts:
        q_text += text.text + "###"
    alist.append(q_name)
    alist.append(q_desc)
    alist.append(q_text)

    w_name = page_bottom.find(id='WName').find('h3').text
    w_descs = page_bottom.find(id='WName').find('p')
    w_texts = page_bottom.find(id='WName').next_sibling.find_all('p')
    w_descs_span = w_descs.find_all('span')
    w_descs_b = w_descs.find_all('b')
    w_desc = w_descs_b[0].text + w_descs_span[0].text + \
        "###" + w_descs_b[1].text + w_descs_span[1].text

    w_text = ""
    for text in w_texts:
        w_text += text.text + "###"
    alist.append(w_name)
    alist.append(w_desc)
    alist.append(w_text)

    e_name = page_bottom.find(id='EName').find('h3').text
    e_descs = page_bottom.find(id='EName').find('p')
    e_texts = page_bottom.find(id='EName').next_sibling.find_all('p')
    e_descs_span = e_descs.find_all('span')
    e_descs_b = e_descs.find_all('b')
    e_desc = e_descs_b[0].text + e_descs_span[0].text + \
        "###" + e_descs_b[1].text + e_descs_span[1].text

    e_text = ""
    for text in e_texts:
        e_text += text.text + "###"
    alist.append(e_name)
    alist.append(e_desc)
    alist.append(e_text)

    r_name = page_bottom.find(id='RName').find('h3').text
    r_descs = page_bottom.find(id='RName').find('p')
    r_texts = page_bottom.find(id='RName').next_sibling.find_all('p')
    r_descs_span = r_descs.find_all('span')
    r_descs_b = r_descs.find_all('b')
    r_desc = r_descs_b[0].text + r_descs_span[0].text + \
        "###" + r_descs_b[1].text + r_descs_span[1].text

    r_text = ""
    for text in r_texts:
        r_text += text.text + "###"
    alist.append(r_name)
    alist.append(r_desc)
    alist.append(r_text)
    champ_dict[champ_key]['abilities'] = alist


def get_data():
    base_url = 'https://universe.leagueoflegends.com'
    extended_url = '/en_US/champions/'
    champ_dict = get_champ_list(base_url, extended_url)
    get_game_info_url(champ_dict)
    key_to_delete = []
    for champ_key in champ_dict:
        champ_url = champ_dict[champ_key]['url']
        get_champ_background(champ_dict, champ_url, champ_key)
        try:
            champ_game_info_url = champ_dict[champ_key]['game_info_url']
        except:
            print('New Champion without information')
            key_to_delete.append(champ_key)
            continue
        get_champ_game_info(champ_dict, champ_game_info_url, champ_key)

    for i in key_to_delete:
        del champ_dict[i]
    return champ_dict

######################### end of the function to fetch champ info  #############################


if __name__ == '__main__':
    ###################### parameters for chromedrive ##########################

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,
             'disk-cache-size': 4096}
    chromeOptions.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    try:
        start_time = datetime.now()
        champs = get_data()
        with open("test_data.json", 'w') as f:
            dumped_json_cache = json.dumps(champs, indent=4)
            f.write(dumped_json_cache)
        print("Total time cost for scraping is ", datetime.now() - start_time)
    except:
        print("Opps, something wrong with scraping web information")
    finally:
        browser.close()
