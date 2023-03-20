url_optim = lambda page: f'https://ies.cloudpss.net:8201/editor/componentheatList/?page={page}'
url_simul = lambda page: f'https://ies.cloudpss.net:8202/editor/componentheatList/?page={page}'

cookie = "first=1; theme=default; TK=4e128a76808f4e283cb57df7d3fd098e18c91354; username=Steven0128; email=; id=1197; setlang=test; setlang1=test213; csrf=y44LdL8zKAS5ekFb0juN8AQIT4sUFULlm6zyM7COSOVS2zCiYTtJGTl7xNmg5s5r; csrftoken=y44LdL8zKAS5ekFb0juN8AQIT4sUFULlm6zyM7COSOVS2zCiYTtJGTl7xNmg5s5r; SECKEY_ABVK=V2LDA8s7CsTqpEEHZq0kuqU2858iImKTRvyL8EiOufY=; BMAP_SECKEY=Gn9oAOjImVjpMeGQEOuqu_xrHDC84iJvz5JxBud_VhUQQVS1iBJqkI86WRnkCULOLt_KIo5kU4WCrWZJtm_Oe2bnhJvCl00DsMoTbcghyXqCHJIPrxd6Y_a8sIT8Dp0u3Hhzwz7pBTPOJKvSNOptaRiOVKwz7FcLw8p45AcPEnT8PogCdZeCZke3JYL5v7VS"

import requests

r = requests.get(url_optim(1), headers={'Cookie':cookie})
print(r.content)