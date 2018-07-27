import json
from datetime import datetime
from requests_html import HTMLSession

from get_url import get_current_mirror


def check_is_end(league, teams, score):
    url = requests.get('http://1xstavka.ru').url + '/getTranslate/ViewGameResultsGroup'
    headers = {'content-type': 'application/json'}
    data = '{"Language":"ru"}{"Params":["%s", null, 85, null, null, 180]}{"Vers":6}{"Adult": false}' % datetime.today().isoformat()[:10]
    teams = [w.strip() for w in teams.split('—')]
    
    response = json.loads(requests.post(url, data=data, headers=headers).text)
    
    for l in response.get('Data')[0].get('Elems'):
        last_couple = l.get('Elems')[-10:]
        for g in last_couple:
            league_str, teams_str = g.get('Head')[4:6]
            teams_str = [w.strip() for w in teams_str.split('-')]
            score_str = [int(g.get('Head')[6][0]), int(g.get('Head')[6][2])]
            if [league_str, teams_str[0], teams_str[1]] == [league, teams[0], teams[1]]:
                return True
    print('Checking end for %s' % teams)
    return False
