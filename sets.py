import csv

NEXT_MATCHES_FILE_NAME = 'next_matches.txt'
UPCOMING_SET_FILE_NAME = 'upcoming.txt'
TEAMS_FILE_NAME = 'teams.txt'
RESULTS_FILES = ['2016_2017.csv']

def load_teams():
    teams = {}
    with open(TEAMS_FILE_NAME) as f:
        lines = f.readlines()
        for line in lines:
            l = line.split(',')
            name = l[0]
            gk = l[1].strip()
            de = l[2].strip()
            mi = l[3].strip()
            at = l[4].strip()
            teams[name] = [gk, de, mi, at]
            print('Name : ' + name)
    return teams

def last_matches_coef(team, matches):
    m = matches[team]
    if len(m) < 5 :
        return
    coef = 0
    for match in m[-5:]:
        if match == 'W':
            coef += 0.2
        elif match == 'D':
            coef += 0.1
    return coef

def create_set():
    teams = load_teams()
    matches = {t : [] for t in teams}
    with open('set.txt', 'w+') as ff:
        for file in RESULTS_FILES:
            with open(file) as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    can_write = False
                    l = row[0].split(';')
                    home_team = l[0]
                    home_stats = teams[home_team]
                    away_team = l[1]
                    away_stats = teams[away_team]
                    res = int(l[4])
                    line = ''
                    for stat in home_stats:
                        line += stat
                        line += ' '
                    for stat in away_stats:
                        line += stat
                        line += ' '
                    home_coef = last_matches_coef(home_team, matches)
                    away_coef = last_matches_coef(away_team, matches)
                    if home_coef and away_coef:
                        line += format(home_coef, '.1f') + ' ' + format(away_coef, '.1f')
                        can_write = True
                    line += ' '
                    if home_coef and away_coef:
                        line += format(home_coef, '.1f') + ' ' + format(away_coef, '.1f')
                        can_write = True
                    if res == 0:
                        matches[home_team].append('D')
                        matches[away_team].append('D')
                        line += ' 0.0 1.0 0.0'
                    elif res == 1:
                        matches[home_team].append('W')
                        matches[away_team].append('L')
                        line += ' 1.0 0.0 0.0'
                    elif res == 2:
                        matches[home_team].append('L')
                        matches[away_team].append('W')
                        line += ' 0.0 0.0 1.0'
                    line += '\n'
                    if can_write:
                        ff.write(line)
            with open(TEAMS_FILE_NAME, 'w+') as f:
                for team in teams:
                    line = team + ','
                    for attr in teams[team]:
                        line += str(attr) + ','
                    line += format(last_matches_coef(team, matches), '.1f') + '\n'
                    f.write(line)

def create_upcoming():
    teams = {}
    with open(TEAMS_FILE_NAME) as f:
        lines = f.readlines()
        for line in lines:
            l = line.split(',')
            name = l[0]
            gk = l[1].strip()
            de = l[2].strip()
            mi = l[3].strip()
            at = l[4].strip()
            coef = l[5].strip()
            teams[name] = [gk, de, mi, at, coef]
    matches = []
    with open(NEXT_MATCHES_FILE_NAME) as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            arr = line.split(':')
            matches.append((arr[0].strip(), arr[1].strip()))
    with open(UPCOMING_SET_FILE_NAME, 'w+') as f:
        for match in matches:
            home_attrs = teams[match[0]]
            away_attrs = teams[match[1]]
            line = ''
            for i in range(4):
                line += str(home_attrs[i]) + ' '
            for i in range(4):
                line += str(away_attrs[i]) + ' '
            line += home_attrs[-1] + ' ' + away_attrs[-1] + ' '
            line += home_attrs[-1] + ' ' + away_attrs[-1] + ' 0.0 0.0 0.0\n'
            f.write(line)

if __name__ == '__main__':
    create_set()
    create_upcoming()
