from fifa_game import FifaLiveGame




def init_games_from_data(data, cur_games, cur_mirror):
    events = data.get('Value')
    first_time_live_events = (event for event in events if is_live(event) and is_first_time(event))

    games = []
    for event in first_time_live_events:
        score = get_score(event)
        if sum_of_score(score) > 3:
            continue

        id = get_id(event)
        teams = get_teams(event)
        time = get_minute(event)
        
        if is_30s_minutes(event) and (id, teams) not in cur_games:
            print(time)
            games.append(FifaLiveGame(id, teams, score, time, event, cur_mirror))

    return games

def get_teams(event):
    return (event.get('O1'), event.get('O2'))

def is_live(event):
    return event.get('SC').get('CPS')
        
def is_first_time(event):
    return get_minute(event) <= 45

def get_minute(event):
    return int(int(event.get('SC').get('TS', 0)) / 60)

def is_30s_minutes(event):
    return str(get_minute(event))[0] == '3' and len(str(get_minute(event))) > 1

def get_id(event):
    return event.get('I')

def sum_of_score(score):
    return sum(score)

def get_score(event):
    return (event.get('SC').get('FS').get('S1', 0), event.get('SC').get('FS').get('S2', 0))
