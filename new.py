import requests
import requests_cache
from urllib.parse import urljoin
from datetime import date, timedelta
from collections import namedtuple


URL = 'https://api.github.com'

# URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20
repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues'])

def get_trending_repositories(url):
    html = requests.get(url)
    #Теперь записываешь файл
    content = html.text
    try:
        with open('page_cache.txt', mode='tw', encoding='utf-8') as file_handler:
            file_handler.write(content)
    except EnvironmentError as err:
        print(err)


if __name__ == '__main__':
    requests_cache.install_cache('page_cache', backend='sqlite', expire_after=10)
    # requests_cache.clear()

    days_interval, repositories_limit, url = DAYS_INTERVAL, REPOSITORIES_LIMIT, URL
    search_url = urljoin(url, 'search/repositories')

    days_ago = (date.today() - timedelta(days=days_interval)).isoformat()
    params = {'q': 'created:>{}'.format(days_ago),
              'sort': 'stars',
              'per_page': str(repositories_limit),
              'order': 'desc'
              }
    #requests_cache.clear()
    r = requests.get(search_url, params=params)
    print(r.from_cache)

    repositories_info = r.json()["items"]


    # html = requests.get(URL)
    print(repositories_info)