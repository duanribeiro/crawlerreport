import time

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor


class GetterPJE502(scrapy.Spider):
    name = 'GetterPJE502'
    start_urls = [
        'https://consulta.pje.trtsp.jus.br/acesso/acesso.pl'
    ]

    def captcha_recaptcha(self, sitekey, url, invisible=1):
        json_create = {
            "key": '20b930f4e71b65e1c4584b7578d3e7dd',
            "method": 'userrecaptcha',
            "googlekey": sitekey,
            "pageurl": url,
            "appear": 1,
            "hear": "now",
            "json": 1
        }
        if invisible:
            json_create['invisible'] = 1

        r_create = requests.post('http://2captcha.com/in.php', data=json_create).json()
        if r_create['status'] == 0:
            return False, r_create['request']

        taskId = r_create['request']
        url_result = "http://2captcha.com/res.php?key=20b930f4e71b65e1c4584b7578d3e7dd&action=get&id=" + \
                     taskId + "&json=0"

        while requests.get(url_result).content.decode("utf-8") == 'CAPCHA_NOT_READY':
            time.sleep(5)

        resposta = requests.get(url_result).content.decode("utf-8")
        if len(resposta) < 45:
            return False, resposta

        return True, resposta.split('|')[1]

    def parse(self, response):
        self.url = 'https://consulta.pje.trtsp.jus.br/acesso/acesso.pl'

        captcha_key = response.xpath('//*[@class="g-recaptcha"]').attrib['data-sitekey']
        status, captcha_text = self.captcha_recaptcha(captcha_key, self.url)
        recipes = LinkExtractor(allow=r'/www/\d+/.*').extract_links(response)
        self.driver.execute_script('document.getElementById("g-recaptcha-response").style.display = ""')
        self.driver.find_element_by_id('g-recaptcha-response').send_keys(token_value)
        self.driver.find_element_by_name('btnSubmeterProcessos').click()

        iframe = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LeeqScTAAAAAF7EJCM2X0i8ar3_R-' \
                 'n3fs5I1Zyc&co=aHR0cHM6Ly9jb25zdWx0YS5wamUudHJ0c3AuanVzLmJyOjQ0Mw..&hl=pt-BR&v=v155' \
                 '5968629716&size=normal&cb=1eqh89kkec16'

        x = scrapy.Request(a)

        pass
