import cProfile, pstats, io
from requests_crawler.GetterESAJ826ByName import GetterESAJ826ByName




urls = [
    "http://esaj.tjsp.jus.br/cpopg/search.do"
]
name_list = [
    'TELEFONICA SA',
    'VIVO BRASIL SA',
    'TELESP SA',
    'COMMCENTER SA',
    'GLOBAL VILLAGE TELECOM',
    'TELECOMUNICACOES DE SAO PAULO'
]

requests = GetterESAJ826ByName(name_list=name_list, url=urls[0])


result = requests.run()
print('a')