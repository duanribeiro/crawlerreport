import scrapy
from scrapy.linkextractors import LinkExtractor


class GetterESAJ826ByName(scrapy.Spider):
    name = 'GetterESAJ826ByName'

    def start_requests(self):
        urls = [
            "http://esaj.tjsp.jus.br/cpopg/open.do"
        ]

        request_get_params = {
            'dadosConsulta.localPesquisa.cdLocal': '100',
            'cbPesquisa': 'NMPARTE',
            'dadosConsulta.tipoNuProcesso': 'UNIFICADO',
            'dadosConsulta.valorConsulta': 'TELEFONICA SA',
            'chNmCompleto': 'true'
        }

        for url in urls:
            yield scrapy.http.FormRequest(url=url,
                                          method='GET',
                                          callback=self.parse,
                                          formdata=request_get_params)

    def parse(self, response):
        response.xpath('//*[@id="listagemDeProcessos"]')
        x = scrapy.linkextractors('')

        pass
