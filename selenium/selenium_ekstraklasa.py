from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import getpass
import datetime

players_df = pd.DataFrame(
    {'player_name': [],'season': [], 'team': [], 'games_played': [], 'goals': [], 'assists': [], 'y_card': [], 'r_card': []})

# Init:
gecko_path = '/opt/homebrew/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.flashscore.pl/pilka-nozna/polska/pko-bp-ekstraklasa/#/4fofM1vn/table/overall'

# Actual program:
time.sleep(3)

driver.get(url)

time.sleep(3)
# Find the table containing the teams
teams_table = driver.find_element(By.XPATH, '//*[@id="tournament-table-tabs-and-content"]')
# Find all the links to teams within the table rows
team_links = teams_table.find_elements(By.CLASS_NAME, "tableCellParticipant__name")
#Extract all hrefs
team_links_hrefs = [link.get_attribute('href') for link in team_links]
print("List of teams:", team_links_hrefs)

# Extract and print the URLs
for team_url in team_links_hrefs:
    #print(team_url)
    time.sleep(5)
    driver.get(team_url)
    time.sleep(2)
    squad = driver.find_element(By.XPATH, '//*[@id="li6"]')
    squad_link = squad.get_attribute('href')
    #print('Squad link', squad_link)
    time.sleep(2)
    driver.get(squad_link)
    time.sleep(2)

    player_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/zawodnik/']")
    # Extract the URLs from the links
    player_urls = [link.get_attribute("href") for link in player_links]
    coach_link = player_urls[-1] #get coach link

    players_urls = list(set(player_urls))  # removing duplicates and coach
    players_urls.remove(coach_link)

    for player_link in players_urls:

        driver.get(player_link)
        if len(driver.find_elements(By.XPATH, '//*[@id="league-table"]'))>0:

            div_element = driver.find_element(By.XPATH, '//*[@id="league-table"]')

            row_of_career_table = div_element.find_element(By.XPATH, '//*[@id="league-table"]/div[2]')

            player_name = row_of_career_table.find_element(By.XPATH,'//*[@id="mc"]/div[4]/div[1]/div[2]/div[1]/div[1]').text
            season = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[1]').text
            team = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[2]').text
            games_played = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[4]').text
            goals = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[5]').text
            assists = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[6]').text
            y_card = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[7]').text
            r_card = row_of_career_table.find_element(By.XPATH, '//*[@id="league-table"]/div[2]/div[8]').text

            player_info = {'player_name': player_name, 'season': season, 'team': team, 'games_played': games_played, 'goals': goals, 'assists': assists,
                           'y_card': y_card, 'r_card': r_card}

            players_df = players_df._append(player_info, ignore_index=True)

print(players_df)
# Close the browser
driver.quit()
