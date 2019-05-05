import re
from datetime import datetime

import math
import requests
from bs4 import BeautifulSoup

from utils import hasNumbers


class GetterESAJ826ByName():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.result = []


    def chamada_web(self, comarca, page=1):
        try:
            request_get_params = {
                'paginaConsulta': str(page),  # Número da paginação
                'cbPesquisa': 'NMPARTE', # Filtro de pesquisa
                'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
                'dadosConsulta.valorConsulta': self.name, # String nome da parte
                'chNmCompleto': 'true', # Busca por nome completo
                'dadosConsulta.localPesquisa.cdLocal': str(comarca) # Comarca
            }
            response = requests.get(url=self.url, params=request_get_params)
            self.serializa_processos(response=response)

            return response
        except Exception as ex:
            print(f'(primeira_chamada_web) - {ex} ')


    def processa_chamada_web(self, response):
        max_pages = 1
        soup = BeautifulSoup(response.content, features="lxml")

        if 'Não existem informações disponíveis para os parâmetros informados.' in response.text:
            self.result.append({self.name: 'não existem informações'})

        elif 'Foram encontrados muitos processos para os parâmetros informados.' in response.text:
            self.result.append({self.name: 'encontrados muitos processos'})
        else:
            try:
                pagination = soup.find(class_='resultadoPaginacao')
                max_pages = math.ceil(int(pagination.text.replace('\n', '').replace('\t', '').split(' ')[-1]) / 25) + 1
            except:
                pass
        return max_pages


    def chamada_web_paginacao(self, comarca, max_pages):
        for page in range(1, max_pages):
            request_get_params = {
                'paginaConsulta': str(page),
                'cbPesquisa': 'NMPARTE',
                'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
                'dadosConsulta.valorConsulta': self.name,
                'chNmCompleto': 'true',
                'dadosConsulta.localPesquisa.cdLocal': str(comarca)
            }
            response = requests.get(url=self.url, params=request_get_params, verify=False)
            self.serializa_processos(response=response)

        return self.result


    def serializa_processos(self, response):
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

                self.result.append({self.name:
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
            except:
                print(f'Pattern não reconhecido -> CNJ: {fields[0]}')


