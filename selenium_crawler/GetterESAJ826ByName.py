import cProfile as profile

# In outer section of code
pr = profile.Profile()
pr.disable()

# In section you want to profile
pr.enable()




from datetime import datetime
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetterESAJ826ByName():
    def __init__(self, name_list, url):
        self.name_list = name_list
        self.url = url
        self.driver = webdriver.Chrome('driver/chromedriver.exe')

    def run(self):
        return_object = []

        for name in self.name_list:
            self.driver.get(self.url)
            self.driver.find_element_by_xpath('//*[@id="id_Foro"]/option[9]').click()  # Foro Central Cívil
            self.driver.find_element_by_xpath('//*[@id="cbPesquisa"]/option[2]').click()
            self.driver.find_element_by_id('campo_NMPARTE').clear()
            self.driver.find_element_by_id('campo_NMPARTE').send_keys(name)
            self.driver.find_element_by_id('pbEnviar').click()

            if 'Foram encontrados muitos processos para os parâmetros informados.' in self.driver.page_source:
                return_object.append({name: 'encontrados muitos processos'})
                continue
            elif 'Não existem informações disponíveis para os parâmetros informados.' in self.driver.page_source:
                return_object.append({name: 'não existem informações'})
                continue
            max_pages = math.ceil(
                int(self.driver.find_element_by_xpath('//*[@id="paginacaoSuperior"]/tbody/tr[1]/td[1]')
                    .text.split(' ')[-1]) / 25)

            for page in range(1, max_pages + 1):
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "listagemDeProcessos"))
                )

                self.driver.find_element_by_id('listagemDeProcessos')

                lawsuits = [x.text for x in self.driver.find_element_by_id('listagemDeProcessos')
                    .find_elements_by_xpath('//div[@id[starts-with(.,"divProcesso")]]')]
                for lawsuit in lawsuits:
                    fields = lawsuit.split('\n')

                    # É preciso associar as informações, pois cada processo tem um 'pattern'
                    if len(fields) == 5:
                        i, j = 3, 1
                    if len(fields) == 4:
                        try:
                            i, j = 3, 1
                            datetime.strptime(fields[i].strip().split('-')[0][-11:].strip(), '%d/%m/%Y')
                        except:
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

                if self.driver.find_elements_by_link_text('>'):
                    self.driver.find_element_by_link_text('>').click()

        return return_object

if __name__ == '__main__':



    # Back in outer section of code
    pr.dump_stats('profile.pstat')
    name_list = [
        'GVT SA',
        'TELEFONICA SA',
        'VIVO BRASIL SA',
        'TELESP SA',
        'COMMCENTER SA',
        'GLOBAL VILLAGE TELECOM',
        'TELECOMUNICACOES DE SAO PAULO'
    ]
    urls = [
        "http://esaj.tjsp.jus.br/cpopg/open.do"
    ]

    for url in urls:
        get826 = GetterESAJ826ByName(name_list=name_list, url=url)
        result = get826.run()

    # code of interest
    pr.disable()
    # Back in outer section of code
    pr.print_stats()
    pr.dump_stats('profile.pstat')