from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
from Player import Player


def get_team_url_sufixs(league_url):
	with urlopen(league_url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		selectedCountryList = soup.find(class_="menu selected-country-list").find(class_='head')
		countryName = selectedCountryList.text
		rows = soup.find(id='tournament-page-participants').tbody.find_all('tr')
		for td in rows:
			print(td.text)
			yield td.a['href']
			
			
def get_team_members_page_url(team_url_sufix):
	print(team_url_sufix)
	return baseUrl + team_url_sufix + '/sklad'
	
def get_players_for_team(team_url):
	with urlopen(team_url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		rows = soup.find(id='fsbody').table.tbody.find_all('tr')
		for tr in rows:
			player_number_cell = tr.find(class_='jersey-number')
			if None != player_number_cell and not player_number_cell.text: #omit traineer
				continue
			player_name_cell = tr.find(class_='player-name')
			player_age_cell = tr.find(class_='player-age')
			if None != player_name_cell and None != player_age_cell:
				country = player_name_cell.span['title']
				name = player_name_cell.text
				age = player_age_cell.text
				description = f'{name} - {age} - {country}'
				print(description)

if __name__ == '__main__':
	baseUrl = 'http://www.flashscore.pl'
	league_url = baseUrl + '/pilka-nozna/anglia/premier-league/zespoly/'

	for team_url_sufix in get_team_url_sufixs(league_url):
		team_url = get_team_members_page_url(team_url_sufix)
		get_players_for_team(team_url)
		sleep(10)
	