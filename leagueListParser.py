import urllib.request
from bs4 import BeautifulSoup
baseUrl = 'http://www.flashscore.pl'
league_url = baseUrl + '/pilka-nozna/anglia/premier-league/zespoly/'

def get_team_url_sufixs(league_url):
	with urllib.request.urlopen(league_url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		rows = soup.find(id='tournament-page-participants').tbody.find_all('tr')
		for td in rows:
			yield td.a['href']
			
			
def get_team_members_page_url(team_url_sufix):
	print(team_url_sufix)
	return baseUrl + team_url_sufix + '/sklad'
	
def get_players_for_team(team_url):
	with urllib.request.urlopen(team_url) as f:
		html = f.read()
		soup = BeautifulSoup(html, 'html.parser')
		rows = soup.find(id='fsbody').table.tbody.find_all('tr')
		for tr in rows:
			player_name_cell = tr.find(class_='player-name')
			player_age_cell = tr.find(class_='player-age')
			if None != player_name_cell and None != player_age_cell:
				country = player_name_cell.span['title']
				name = player_name_cell.text
				age = player_age_cell.text
				description = f'{name} - {age} - {country}'
				print(description)

for team_url_sufix in get_team_url_sufixs(league_url):
	team_url = get_team_members_page_url(team_url_sufix)
	get_players_for_team(team_url)
	