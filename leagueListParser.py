from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
from Player import Player
from Team import Team
from CsvWriter import CsvWriter
from datetime import datetime, timedelta

base_url = "http://www.flashscore.pl"

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
	return base_url + team_url_sufix + '/sklad'
	
def get_players_for_team(team):
	with urlopen(team.url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find(id='fsbody').table
		if None ==  table:
			return
		tbody = table.tbody
		if None == tbody:
			return
		rows = tbody.find_all('tr')		
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
				birth_date = get_player_birth_date(player_name_cell.a['href'])
				yield Player(team, name, birth_date, country, currentParsingPosition)

def get_player_birth_date(player_url_sufix):
	url = base_url + player_url_sufix
	with urlopen(url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		birthdate_div = soup.find(class_='player-birthdate')
		if None == birthdate_div:
			return ""
		birthdate_scirpt = birthdate_div.script.text
		start_index = birthdate_scirpt.find("Age(") + 4
		end_index = birthdate_scirpt.find(')', start_index)
		unitTimeStamp = int(birthdate_scirpt[start_index:end_index]) + 12 * 3600

		if unitTimeStamp < 0:
			date = datetime(1970, 1, 1) + timedelta(seconds=unitTimeStamp)
		else:
			date = datetime.fromtimestamp(unitTimeStamp)

		return date.strftime('%Y-%m-%d')

def get_urls_to_parse():
	with open('input.txt') as f:
		for line in f:
			yield line

def get_file_name_from_url(url):
	splitted_url = url.split('/')
	return splitted_url[-4] + "+" + splitted_url[-3] + ".csv"

if __name__ == '__main__':
	for url in get_urls_to_parse():
		file_name = get_file_name_from_url(url)
		with CsvWriter(file_name) as csv:
			csv.add("Kraj", "Liga", "Klub", "Imie i nazwisko", "Data urodzenia", "Narodowość", "Pozycja")		
			for team in get_teams_infos(url):
				print(team.name)
				for player in get_players_for_team(team):
					csv.add(player.playingCountry, player.leagueName, player.teamName, player.fullName, player.age, player.nationality, player.position)
				sleep(2)



