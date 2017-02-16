NUM_OF_TEAMS = 20

PLAYERS_FILE_NAME = 'players.txt'
CHANCE_FILE_NAME = 'chance_of_playing.txt'

def load_active():
    players = dict()
    with open(CHANCE_FILE_NAME) as f:
        lines = f.readlines()
        for l in lines:
            name = l.split(',')[0]
            pos = int(l.split(',')[2].strip())
            players[name] = pos
    return players

class Team:
    def __init__(self, name):
        self.name = name
        self.gks = []
        self.defs = []
        self.mids = []
        self.atts = []

    def gks_rating(self):
        n = len(self.gks)
        if not n:
            n = 1
        return float(sum(self.gks)) / n

    def defs_rating(self):
        n = len(self.defs)
        if not n:
            n = 1
        return float(sum(self.defs)) / n

    def mids_rating(self):
        n = len(self.mids)
        if not n:
            n = 1
        return float(sum(self.mids)) / n

    def atts_rating(self):
        n = len(self.atts)
        if not n:
            n = 1
        return float(sum(self.atts)) / n

    def str(self):
        return name + ' : [' + str(self.gks_rating()) + ', ' + str(self.defs_rating()) + ', ' + str(self.mids_rating()) + ', ' + str(self.atts_rating()) + ']'

def teams():
    active = load_active()
    teams = {}
    with open(PLAYERS_FILE_NAME) as f:
        lines = f.readlines()
        for line in lines:
            spl = line.split(',')
            name = spl[0].strip()
            team = spl[1].strip()
            rating = int(spl[3].strip())
            if not teams.get(team):
                teams[team] = Team(team)
            if name in active:
                pos = active[name]
                #print('Name : ' + name + '   Pos : ' + str(pos))
                if pos == 1:
                    #print('Add to team ' + team + ' add gk : ' + str(rating))
                    teams[team].gks.append(rating)
                elif pos == 2:
                    teams[team].defs.append(rating)
                elif pos == 3:
                    teams[team].mids.append(rating)
                elif pos == 4:
                    teams[team].atts.append(rating)
    print('Teams : ' + str(len(teams)))
    return teams
                
def normalize(teams):
    tms = list(teams.values())
    min_gks_rat = min([t.gks_rating() for t in tms])
    max_gks_rat = max([t.gks_rating() for t in tms])
    min_defs_rat = min([t.defs_rating() for t in tms])
    max_defs_rat = max([t.defs_rating() for t in tms])
    min_mids_rat = min([t.mids_rating() for t in tms])
    max_mids_rat = max([t.mids_rating() for t in tms])
    min_atts_rat = min([t.atts_rating() for t in tms])
    max_atts_rat = max([t.atts_rating() for t in tms])

    with open('teams.txt', 'w+') as f:
        for t in tms:
            gk = (t.gks_rating() - min_gks_rat) / (max_gks_rat - min_gks_rat)
            de = (t.defs_rating() - min_defs_rat) / (max_defs_rat - min_defs_rat)
            mi = (t.mids_rating() - min_mids_rat) / (max_mids_rat - min_mids_rat)
            at = (t.atts_rating() - min_atts_rat) / (max_atts_rat - min_atts_rat)

            line = '{}, {}, {}, {}, {}\n'.format(t.name, gk, de, mi, at)
            f.write(line)

if __name__ == '__main__':
    t = teams()
    normalize(t)
