import time
from datetime import datetime
from collections import deque


import get_url
import get_data
import init_games
import send_to_chanell



if __name__ == "__main__":
    print("Starts working...")

    leagues_games_cnt = {
        'FIFA 17. Europe League': 0,
        'FIFA 17. Champions League': 0
    }

    cur_games = deque(maxlen=3)
    cur_games_tuples = deque(maxlen=3)
    sended_games = deque(maxlen=3)
    while True:
        cur_time = datetime.now().time()
        if cur_time.hour + 3 == 0 and cur_time.minute in range(0, 10):
            leagues_games_cnt = dict.fromkeys(leagues_games_cnt, 0)
        cur_mirror = get_url.get_current_mirror()
        if not cur_mirror:
            print("Will sleep 10 second because of url")
            time.sleep(10)
            continue

        data = get_data.get_live_data(cur_mirror)
        if not data:
            print("Sleep")
            time.sleep(10)
            continue

        for g in cur_games:
            if (g.id, g.teams) not in cur_games_tuples:
                cur_games_tuples.append((g.id, g.teams))

        new_games = init_games.init_games_from_data(data, cur_games_tuples, cur_mirror)
        if len(new_games) > 0:
            print(f"Found {len(new_games)} new games")

        for g in new_games:
            try:
                g.fill_data_by_id()
            except Exception as e:
                print('Error in fill_data_by_id')
                continue
            g.fill_target_coef()
            if g.target_coef == -1:
                print(f"Deleting {g.teams} because coef == -1")
                del g

        for g in cur_games:
            try:
                g.fill_data_by_id()
            except Exception as e:
                print('Error in fill_data_by_id')
                continue
            if g.is_target() and (g.id, g.teams) not in sended_games and g.target_coef >= 1.5:
                teams = g.teams
                coef = g.target_coef
                score = g.score
                total = g.total
                league = g.league
                leagues_games_cnt[league] += 1
                print(f"Sending: {teams}: {coef}")
                send_to_chanell.send_msg(f"""Номер игры: {leagues_games_cnt.get(league)}
{league}
{teams[0]} - {teams[1]}
Кф: {coef} на {total}б
Счёт на 45-й: {score[0]}:{score[1]}""")
                sended_games.append((g.id, teams))
                cur_games_tuples.remove((g.id, g.teams))
                del g
                continue
            if g.is_second_half() and g in cur_games:
                cur_games_tuples.remove((g.id, g.teams))
                del g

        cur_games.extend(new_games)
