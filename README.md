# League of Legends Project

Project using Selenium, Beatiful Soup, Sqlite3 and Plotly API to scrape data and provide users with interactive prompt for search they like.

## Data Source

  - https://universe.leagueoflegends.com/en_US/champions/ 
  - https://na.leagueoflegends.com/en/game-info/champions/

## Information needed  to run this program
  - [Selenium] ( A python module used to scraping dynamical websites generated by JS.)
  - [Chromedriver] ( A must for Seleinum on Chrome.)
  - [Sqlite3] ( SQL used to build the database.)
  - [Beautiful Soup] ( A faster tool to get the specific information after scraping the page element.)
  - [Plotly] ( Need a API to use plotly.)

## Program structure
  - Class:
    - Champ (used to store the champion information)
  - Function:
    - process_normal_command(command_list)
    - process_compare_command(champ1, champ2)
  - Data structure:
    - List: to store the champion panel properties
    - Dicitionary: to store the skills of champions

## User Guide
  - Make sure download all the stuff including the database and json file so that you won't to run redo the scraping and building databases.
  - Create virtual environment and install all the dependencies
    ```
    $ virtualenv -p python3 <path_of_virtual_env>
    $ pip install requirement.txt
  - Run this line to activate the virtual environment
    ```
    $ source <path_of_virtual_env>/bin/activate
  - In this virtual environment, run this line
    ``` 
    $ python league_of_legends.py
  - Based on the prompt, do the search and have fun.

[//]: # 
   [Selenium]: <https://www.seleniumhq.org/>
   [Chromedriver]:<http://chromedriver.chromium.org/>
   [Sqlite3]:<https://www.sqlite.org/>
   [Beautiful Soup]:<https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
   [Plotly]:<https://plot.ly/python/>
