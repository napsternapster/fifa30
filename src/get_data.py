import json

from requests_html import HTMLSession


def get_live_data(cur_mirror):
    url = f"{cur_mirror}/LiveFeed/Get1x2_Zip?sports=85&count=1000&mode=4&"
    session = HTMLSession()
    try:
        json_data = session.get(url, timeout=10).text
    except Exception as e:
        print('Exception while getting data from 1xstavka.')
        return []
    data = json.loads(json_data)
    return data
