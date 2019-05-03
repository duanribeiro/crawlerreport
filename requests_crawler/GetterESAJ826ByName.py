import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

urls = [
    "http://esaj.tjsp.jus.br/cpopg/search.do"
]

name_list = [
    'GVT SA',
    'TELEFONICA SA',
    'VIVO SA',
    'TELESP SA',
    'COMMCENTER SA',
    'GLOBAL VILLAGE TELECOM',
    'TELECOMUNICACOES DE SAO PAULO'
]


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


return_object = []

for url in urls:
    for name in name_list:
        request_get_params = {
            'paginaConsulta': '1',
            'cbPesquisa': 'NMPARTE',
            'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
            'dadosConsulta.valorConsulta': name,
            'chNmCompleto': 'true',
            'dadosConsulta.localPesquisa.cdLocal': '100'
        }
        response = requests.get(url=url, params=request_get_params)
        soup = BeautifulSoup(response.content, features="lxml")

        if 'Não existem informações disponíveis para os parâmetros informados.' in response.text:
            return_object.append({name: 'não existem informações'})
            continue
        elif 'Foram encontrados muitos processos para os parâmetros informados.' in response.text:
            return_object.append({name: 'encontrados muitos processos'})
            continue

        pagination = soup.find(class_='resultadoPaginacao')
        max_pages = round(int(pagination.text.replace('\n', '').replace('\t', '').split(' ')[-1]) / 25) + 1

        for page in range(1, max_pages):
            if page != 1:
                request_get_params = {
                    'paginaConsulta': str(page),
                    'cbPesquisa': 'NMPARTE',
                    'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
                    'dadosConsulta.valorConsulta': name,
                    'chNmCompleto': 'true',
                    'dadosConsulta.localPesquisa.cdLocal': '100'
                }
                response = requests.get(url=url, params=request_get_params)
                soup = BeautifulSoup(response.content, features="lxml")

            lawsuits = soup.find_all("div", {"id": re.compile('divProcesso')})
            i = 0
            for lawsuit in lawsuits:
                i += 1
                print(i)
                try:
                    fields = [x.strip() for x in lawsuit.text.replace('\n', '').replace('\t', '').split('  ') if x]

                    # Pattern 1
                    if len(fields) == 5:
                        if hasNumbers(fields[1]):
                            return_object.append({name:
                                {
                                    'data_coleta': datetime.now(),
                                    'CNJ': fields[0].strip(),
                                    'parte_passiva': None,
                                    'parte_ativa': None,
                                    'recebimento': datetime.strptime(fields[3].strip().split('-')[0][-11:].strip(),
                                                                     '%d/%m/%Y'),
                                    'vara': fields[3].split('-')[1].strip().title(),
                                    'classe': fields[2].split('/')[0].strip().title()
                                }
                            })

                        # Pattern 2
                        else:
                            return_object.append({name:
                                {
                                    'data_coleta': datetime.now(),
                                    'CNJ': fields[0].strip(),
                                    'parte_passiva': None,
                                    'parte_ativa': None,
                                    'recebimento': datetime.strptime(fields[4].strip().split('-')[0][-11:].strip(),
                                                                     '%d/%m/%Y'),
                                    'vara': fields[4].split('-')[1].strip().title(),
                                    'classe': fields[1].split('/')[0].strip().title()
                                }
                            })
                    # Pattern 3
                    if len(fields) == 4:
                        return_object.append({name:
                            {
                                'data_coleta': datetime.now(),
                                'CNJ': fields[0].strip(),
                                'parte_passiva': None,
                                'parte_ativa': None,
                                'recebimento': datetime.strptime(fields[2].strip().split('-')[0][-11:].strip(),
                                                                 '%d/%m/%Y'),
                                'vara': fields[2].split('-')[1].strip().title(),
                                'classe': fields[1].split('/')[0].strip().title()
                            }
                        })

                except Exception as ex:
                    print(ex)
print('a')
