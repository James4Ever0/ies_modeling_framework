url_optim = lambda page: f'https://ies.cloudpss.net:8201/editor/componentheatList/?page={page}'
url_simul = lambda page: f'https://ies.cloudpss.net:8202/editor/componentheatList/?page={page}'

import requests

r = requests.get(url_optim(1))


data = r.
import rich
rich.print(data)