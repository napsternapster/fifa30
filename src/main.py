import time
from collections import deque


import get_url
import get_data
import init_games
import send_to_chanell


if __name__ == "__main__":
    print("Starts working...")
    cur_games = deque(maxlen=10)
    cur_games_tuples = deque(maxlen=10)
    sended_games = deque(maxlen=10)
    while True:
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
            if (g.id, g.teams) not in cur_games:
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
            print(g.target_coef)
            print(g.total)
            if g.target_coef == -1:
                print(f"Deleting {g.teams} because coef == -1")
                del g

        for g in cur_games:
            try:
                g.fill_data_by_id()
            except Exception as e:
                print('Error in fill_data_by_id')
                continue
            if g.is_target() and (g.id, g.teams) not in sended_games and g.target_coef > 1.5:
                teams = g.teams
                coef = g.target_coef
                score = g.score
                total = g.total
                league = g.league
                print(f"Sending: {teams}: {coef}")
                print(f"League: {league}")
                print(f"""Лига: {league}
{teams[0]} - {teams[1]}
Коэфф на 30-й минуте: {coef}
Тотал: {total}б
Счёт на 45-й: {score[0]}:{score[1]}""")
                send_to_chanell.send_msg(f"""Лига: {league}
{teams[0]} - {teams[1]}
Коэфф на 30-й минуте: {coef}
Тотал: {total}б
Счёт на 45-й: {score[0]}:{score[1]}""")
                sended_games.append((g.id, teams))
        
        cur_games.extend(new_games)
