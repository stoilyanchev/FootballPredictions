import requests
import unicodedata

FILE_NAME = 'players.txt'
URL_TMPL = 'https://www.easports.com/uk/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22page%22:{},%22club%22:%221,5,7,9,10,11,12,17,18,19,95,106,109,1795,1796,1799,1806,1943,1952,1960%22,%22position%22:%22GK,LF,CF,RF,ST,LW,LM,CAM,CDM,CM,RM,RW,LWB,LB,CB,RB,RWB%22%7D'


def load_players():
    pages = 36
    saved_players = set()
    with open(FILE_NAME, 'w+') as f:
        page = 1
        saved_players = set()
        while page <= pages:
            print("Page : " + str(page))
            url = URL_TMPL.format(page)
            print('URL : ' + url)
            try:
                r = requests.get(url)
                json = r.json()
                for player in json['items']:
                    first_name = unicodedata.normalize('NFKD', u"%s"%player['firstName']).encode('ascii','ignore').strip().decode('utf-8')
                    last_name = unicodedata.normalize('NFKD', u"%s"%player['lastName']).encode('ascii','ignore').strip().decode('utf-8')
                    position = player['position']
                    club = player['club']['name']
                    rating = player['rating']

                    name_to_save = '{} {}'.format(first_name, last_name)

                    if name_to_save not in saved_players:
                        saved_players.add(name_to_save)
                        line = '{} {}, {}, {}, {}\n'.format(first_name, last_name,
                                    club, position, str(rating))
                        #print('Player : ' + line)
                        f.write(line)
                page += 1
            except requests.exceptions.RequestException as e:
                print(e)
                return

if __name__ == '__main__':
    load_players()
