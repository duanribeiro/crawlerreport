import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

return_object = []
urls = [
    "http://esaj.tjsp.jus.br/cpopg/search.do"
]
name_list = [
    'GVT SA',
    'TELEFONICA SA',
    'VIVO BRASIL SA',
    'TELESP SA',
    'COMMCENTER SA',
    'GLOBAL VILLAGE TELECOM',
    'TELECOMUNICACOES DE SAO PAULO'
]
for url in urls:
    for name in name_list:
        request_get_params = {
            'paginaConsulta': '1',  # Número da paginação
            'cbPesquisa': 'NMPARTE', # Filtro de pesquisa
            'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
            'dadosConsulta.valorConsulta': name, # String nome da parte
            'chNmCompleto': 'true', # Busca por nome completo
            'dadosConsulta.localPesquisa.cdLocal': '100' # Comarca
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
            for lawsuit in lawsuits:
                try:
                    fields = [x.strip() for x in lawsuit.text.replace('\n', '').replace('\t', '').split('  ') if x]

                    # É preciso associar as informações, pois cada processo tem um 'pattern'
                    if len(fields) == 6:
                        i, j = 5, 2
                    if len(fields) == 5:
                        if hasNumbers(fields[1]):
                            i, j = 3, 2
                        else:
                            i, j = 4, 1
                    if len(fields) == 4:
                        i, j = 2, 1

                    return_object.append({name:
                        {
                            'data_coleta': datetime.now(),
                            'CNJ': fields[0].strip(),
                            'parte_passiva': None,
                            'parte_ativa': None,
                            'recebimento': datetime.strptime(fields[i].strip().split('-')[0][-11:].strip(),
                                                             '%d/%m/%Y'),
                            'vara': fields[i].split('-')[1].strip().title(),
                            'classe': fields[j].split('/')[0].strip().title()
                        }
                    })
                except Exception as ex:
                    print(f'Pattern não encontrado - {fields[0]}')

print('Processo completo!')