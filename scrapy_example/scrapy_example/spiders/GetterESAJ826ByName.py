# -*- coding: utf-8 -*-
import scrapy


class Getteresaj826bynameSpider(scrapy.Spider):
    name = 'GetterESAJ826ByName'
    allowed_domains = ['http://esaj.tjsp.jus.br/cpopg/']

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

    def run(self, response):
        reponse.xpath('//*[@id="paginacaoSuperior"]/tbody/tr[1]/td[1]/h2/span')



