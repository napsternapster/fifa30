from requests_html import HTMLSession



def get_current_mirror():
    """
    Returns current available mirror of the 1xbet.com, 
    first try to redirects, if fails, try to use google
    """
    session = HTMLSession()
    url = 'http://1xstavka.ru'
    try:
        return session.get('http://1xstavka.ru', timeout=10).url.split('?')[0]
    except Exception as e:
        url = 'https://www.google.ru/search?&q=1xbet.com'
        try:
            r = session.get(url, timeout=10)
        except Exception as e:
            print("Can't find current mirror, return empty string")
            return ""

        return r.html.search('⇒ {} ⇒')[0]

