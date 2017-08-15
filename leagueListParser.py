from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
from Player import Player
from Team import Team
from CsvWriter import CsvWriter

def get_teams_infos(league_url):
	with urlopen(league_url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		selectedCountryList = soup.find(class_="menu selected-country-list").find(class_='head')
		countryName = selectedCountryList.text
		leagueName = soup.find(class_='tournament-name').text
		rows = soup.find(id='tournament-page-participants').tbody.find_all('tr')
		for td in rows:
			teamName = td.text
			url = get_team_members_page_url(td.a['href'])
			yield Team(countryName, leagueName, teamName, url)
			
			
def get_team_members_page_url(team_url_sufix):
	return baseUrl + team_url_sufix + '/sklad'
	
def get_players_for_team(team):
	with urlopen(team.url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		rows = soup.find(id='fsbody').table.tbody.find_all('tr')
		currentParsingPosition = ""
		for tr in rows:
			if "player-type-title" in tr['class']:
				currentParsingPosition = tr.td.text
			player_number_cell = tr.find(class_='jersey-number')
			if None != player_number_cell and not player_number_cell.text: #omit traineer
				continue
			player_name_cell = tr.find(class_='player-name')
			player_age_cell = tr.find(class_='player-age')
			if None != player_name_cell and None != player_age_cell:
				country = player_name_cell.span['title']
				name = player_name_cell.text
				age = player_age_cell.text
				yield Player(team, name, age, country, currentParsingPosition)

if __name__ == '__main__':
	baseUrl = 'http://www.flashscore.pl'
	league_url = baseUrl + '/pilka-nozna/anglia/premier-league/zespoly/'
	with CsvWriter('output.csv') as csv:
		csv.add("Kraj", "Liga", "Klub", "Imie i nazwisko", "Wiek", "Narodowość", "Pozycja")		
		for team in get_teams_infos(league_url):
			print(team.name)
			for player in get_players_for_team(team):
				csv.add(player.playingCountry, player.leagueName, player.teamName, player.fullName, player.age, player.nationality, player.position)
			sleep(5)
	