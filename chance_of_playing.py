import requests
import unicodedata

URL_FANTASY = 'https://fantasy.premierleague.com/drf/bootstrap-static'

FILE_NAME = 'chance_of_playing.txt'

def load_players():
    with open(FILE_NAME, 'w+') as f:
        try:
            r = requests.get(URL_FANTASY)
            json = r.json()
            for player in json['elements']:
                first_name = unicodedata.normalize('NFKD', u"%s"%player['first_name']).encode('ascii','ignore').strip().decode('utf-8')
                last_name = unicodedata.normalize('NFKD', u"%s"%player['second_name']).encode('ascii','ignore').strip().decode('utf-8')
                chance = player['chance_of_playing_this_round']
                position_code = player['element_type']
                if not chance:
                    chance = 0
                line = '{} {}, {}, {}\n'.format(first_name, last_name, chance, position_code)
                print('Player : %s'%line)
                f.write(line)
        except requests.exceptions.RequestException as e:
            print(e)
            return
