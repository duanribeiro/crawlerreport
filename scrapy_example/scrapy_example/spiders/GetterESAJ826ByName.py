# -*- coding: utf-8 -*-
import cProfile
import io
import pstats
from datetime import datetime

import scrapy


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        with open('result_scrapy.txt', 'w+') as f:
            f.write(s.getvalue())

        return retval

    return inner


class Getteresaj826bynameSpider(scrapy.Spider):
    name = 'GetterESAJ826ByName'


    def start_requests(self):
        url = "http://esaj.tjsp.jus.br/cpopg/search.do"

        for comarca in range(1, 10):
            request_get_params = {
                'dadosConsulta.localPesquisa.cdLocal': str(comarca),
                'cbPesquisa': 'NMPARTE',
                'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
                'dadosConsulta.valorConsulta': 'TELEFONICA SA',
                'chNmCompleto': 'true'
            }

            yield scrapy.http.FormRequest(url=url,
                                          method='GET',
                                          callback=self.run,
                                          formdata=request_get_params)

    @profile
    def run(self, response):
        return_object = []
        max_pages = 1

        if 'Não existem informações disponíveis para os parâmetros informados.' in response.text:
            return_object.append({'TELEFONICA SA': 'não existem informações'})

        elif 'Foram encontrados muitos processos para os parâmetros informados.' in response.text:
            return_object.append({'TELEFONICA SA': 'encontrados muitos processos'})

        if response.xpath('//*[@id="paginacaoSuperior"]/tbody/tr[1]/td[1]'):
            max_pages = math.ceil(
                int(response.xpath('//*[@id="paginacaoSuperior"]/tbody/tr[1]/td[1]').text.split(' ')[-1]) / 25
            )

        for page in range(1, max_pages + 1):
            lawsuits = response.xpath('//div[@id[starts-with(.,"divProcesso")]]')

            for lawsuit in lawsuits:
                fields = lawsuit.css('div').css('div::text').extract()
                fields = [x.replace('\n', '').replace('\t', '').strip() for x in fields]
                fields = [x for x in fields if x][:5]

                # É preciso associar as informações, pois cada processo tem um 'pattern'
                if len(fields) == 5:
                    i, j = 3, 1

                if len(fields) == 4:
                    try:
                        i, j = 3, 1
                        datetime.strptime(fields[i].strip().split('-')[0][-11:].strip(), '%d/%m/%Y')

                    except:
                        i, j = 2, 1

                return_object.append({'TELEFONICA SA':
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

        return return_object
