import cProfile
import io
import pstats

from requests_example.GetterESAJ826ByName import GetterESAJ826ByName as request_GetterESAJ826ByName

# from pstatsviewer import StatsViewer

url = "http://esaj.tjsp.jus.br/cpopg/search.do"
name_list = [
    'TELEFONICA SA'
    # 'VIVO BRASIL SA',
    # 'TELESP SA',
    # 'COMMCENTER SA',
    # 'GLOBAL VILLAGE TELECOM',
    # 'TELECOMUNICACOES DE SAO PAULO'
]

# PROFILER
pr = cProfile.Profile()
pr.enable()

request_ESAJ826 = request_GetterESAJ826ByName(name_list=name_list, url=url)
result_1 = request_ESAJ826.run()

# selenium_ESAJ826 = selenium_GetterESAJ826ByName(name_list=name_list, url=url)
# result_2 = selenium_ESAJ826.run()


pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
ps.dump_stats('test.prof')
# with open('test_request.', 'w+') as f:
#     f.write(s.getvalue())

# sv = StatsViewer("/path/to/profile.stats")

#snakeviz test.prof
