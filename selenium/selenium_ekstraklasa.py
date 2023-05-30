from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
# Pressing enter:
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import getpass
import datetime

# Init:
gecko_path = '/opt/homebrew/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)
#driver_team = webdriver.Firefox(options = options, service=ser)

url = 'https://www.flashscore.pl/pilka-nozna/polska/pko-bp-ekstraklasa/#/4fofM1vn/table/overall'

# Actual program:
time.sleep(3)

driver.get(url)

time.sleep(5)
# Find the table containing the teams
teams_table = driver.find_element(By.XPATH, '//*[@id="tournament-table-tabs-and-content"]')
# Find all the links to teams within the table rows
team_links = teams_table.find_elements(By.CLASS_NAME, "tableCellParticipant__name")
#Extract all hrefs
team_links_hrefs = [link.get_attribute('href') for link in team_links]
print("List of teams:", team_links_hrefs)

# Extract and print the URLs
for team_url in team_links_hrefs:
    print(team_url)
    time.sleep(5)
    driver.get(team_url)
    time.sleep(2)
    squad = driver.find_element(By.XPATH, '//*[@id="li6"]')
    squad.click()
    time.sleep(2)

    players_table = driver.find_element(By.XPATH, '//*[@id="league-WI1bjKHl-table"]/div')

    players_links = players_table.find_elements(By.CLASS_NAME,"lineup__cell lineup__cell--name")

    for player_link in players_links:
        player_url = player_link.get_attribute('href')
        print(player_url)

# Close the browser
driver.quit()
