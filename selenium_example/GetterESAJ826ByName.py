import math
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class GetterESAJ826ByName():
    def __init__(self, name_list, url):
        self.name_list = name_list
        self.url = url
        self.driver = webdriver.Chrome('selenium_example/driver/chromedriver')

    def run(self):
        return_object = []

        for name in self.name_list:
            for comarca in range(1, 50):
                self.driver.get(self.url)
                self.driver.find_element_by_xpath(f'//*[@id="id_Foro"]/option[{comarca}]').click()  # Foro Central Cívil
                self.driver.find_element_by_xpath('//*[@id="cbPesquisa"]/option[2]').click()
                self.driver.find_element_by_id('campo_NMPARTE').clear()
                self.driver.find_element_by_id('campo_NMPARTE').send_keys(name)
                time.sleep(1)
                self.driver.find_element_by_name('chNmCompleto').click()
                self.driver.find_element_by_id('pbEnviar').click()

                if 'Foram encontrados muitos processos para os parâmetros informados.' in self.driver.page_source:
                    return_object.append({name: 'encontrados muitos processos'})
                    continue
                elif 'Não existem informações disponíveis para os parâmetros informados.' in self.driver.page_source:
                    return_object.append({name: 'não existem informações'})
                    continue

                if self.driver.find_elements_by_xpath('//*[@id="paginacaoSuperior"]/tbody/tr[1]/td[1]'):
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
