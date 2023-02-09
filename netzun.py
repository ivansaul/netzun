import re
import sys
import json
import requests
from tqdm import tqdm
from time import sleep
from pprint import pprint
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NetzunDL:
    def __init__(self, table_of_content: dict):
        self.table_of_content = table_of_content

    def mp4_downloader(self, filename:str, url: str, dest='videos'):
        """
        Download any .mp4  video
        """
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0

        with open(f"{dest}/{filename}.mp4", 'wb') as f:
            for chunk in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='MB', unit_scale=True, desc=filename):
                wrote = wrote + len(chunk)
                f.write(chunk)
        

    def dl_course(self, quality = 'best'):
        """
        Download all videos of course, iterate table_of_content,json from that 
        """
        for k, i in enumerate(self.table_of_content):
            for j in i['capsulas']:
                filename = f"Módulo {k+1} - {j['cap_titulo']}"
                dl_video_url = self.get_dl_video_url(j['vimeo_player_url'], quality = quality)
                
                self.mp4_downloader(filename= filename, url=dl_video_url)

    def get_dl_video_url(self, vimeo_player_url:str , quality = 'best'):
        """
        vimeo_player_url -> https://player.vimeo.com/video/....
        quality -> best, worst

        1. Hacemos un request con a player.vimeo y buscamos todos los mp4
           que se encuentran dentro de "progressive":[mp4] 
           
        2. Ordenamos la lista de diccionarios por quality
        """

        headers = {
            'Referer': 'https://netzun.com/', 
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
            'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.get(vimeo_player_url, headers=headers)
        response = response.text

        # Busca response la #lista después de la palabra "progressive": [#lista] -> #lista
        match = re.search(r'progressive.*?\[(.*?)\]', response)

        if match:
            result = match.group(1)
            result = '['+result+']' # le agregamos [] para convertirlo a lista 
            result = json.loads(result) # 'lista1'

            # ordenamos los videos por quality
            result = sorted(result, key=lambda x: int(x['quality'].rstrip('p')))
            # obnemos solo los link a los videos
            result = [x['url'] for x in result if x['mime']=='video/mp4']
            #pprint(result)   
        else:
            print('No se encontraron los link a los videos.')
        
        if quality == 'best':
            return result[-1]
        else: 
            return result[0]


class Netzun:
    def __init__(self, email, password, url_course):
        self.email = email
        self.password = password
        self.url_course = url_course
        self.login_url = "https://netzun.com/ingresar"
        self.table_of_content = []

    def logout(self):
        self.driver.quit()
    
    def login(self):

        ## Firefox options en modo headless
        #options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        ## initialize the firefox driver
        self.driver = webdriver.Firefox(options=options) 

        # Chrome options en modo headless
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # initialize the chrome driver
        self.driver = webdriver.Chrome("chromedriver", options=options)
        
        # go to netzun login page
        self.driver.get(self.login_url)
    
        # wait for eamil element to be available
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "email")))
        # find email and pass field and insert
        self.driver.find_element(By.NAME,'email').send_keys(self.email)
        self.driver.find_element(By.NAME,'password').send_keys(self.password)
        # click login button
        self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/form/div[2]').click()
        
        # wait for mis-contenidos element to be available
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div[1]/header/nav[1]/ul/li[7]/a')))
        

    def get_source_code(self, url):
        """
        Retorna el codigo fuente de una pagina de netzun a partir de una url
        """
        
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "script")))
        return self.driver.page_source
    
    def get_table_of_content(self):
        """
        Retorna un json que contiene toda la informacion del curso:
        Titulo, Modulo, Tema, url, ....
        """

        html = self.get_source_code(self.url_course)

        soup = BeautifulSoup(html, "html.parser")
        div_modules = soup.find("div", class_="modules")

        li_modules = div_modules.find_all("li", class_=re.compile("accordion__item"))

        for li in li_modules:
            self.table_of_content.append({
                'titulo': li.find("h3").text,
                'n_cap': li.find("p").text,
                'capsulas': [{'cap_titulo': x.text} for x in li.find_all("div", class_="info")]
            })

        # Crea la url para cada video a partir de la url base del curso
        *base_url_course, i, j = url_course.split('/')
        base_url_course, i, j = '/'.join(base_url_course), int(i), int(j)

        for x in self.table_of_content:
            for y in x['capsulas']:
                y['url'] = base_url_course + f"/{i}/{j}"
                # print(base_url_course + f"/{i}/{j}")
                j =j+1
            i = i+1
        
        # Corregir el titulo de las capsulas "Cápsula 3Importa..." -> "Cápsula 3. Importa..."
        for x in self.table_of_content:
            for y in x['capsulas']:
                y['cap_titulo'] = re.sub(r"(\d+)", r"\1. ", y['cap_titulo'])        


        with open('table_of_content.json','w', encoding='utf-8') as file:
            json.dump(self.table_of_content, file, indent=4, ensure_ascii= False)
        
        print(len(self.table_of_content))

        return self.table_of_content


    def add_content_vimeo_url(self):
        i,j = 1, sum([len(x['capsulas']) for x in self.table_of_content])
        for tc in self.table_of_content:
            for c in tc['capsulas']:
                c['vimeo_player_url'] = self.get_vimeo_url(url=c['url'])
                # imprime el recorrido
                print(f"[{i}/{j}]")
                i+=1  

        
        with open('table_of_content.json','w', encoding='utf-8') as file:
            json.dump(self.table_of_content, file, indent=4, ensure_ascii= False)
        
        return self.table_of_content

    def get_vimeo_url(self, url: str):
        """
        Retorna la url del iframe -> player.vimeo.com ....
        a partir de la url del video desde netzum
        """
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.ID, "vimeo-player-1")))

        vimeo = self.driver.find_element(By.ID, "vimeo-player-1")
        vimeo = vimeo.find_element(By.TAG_NAME, 'iframe')
        vimeo = vimeo.get_attribute('src')
        #print(vimeo)
        return vimeo


if __name__ == "__main__":

    # Netzun credentials
    email = "bopil28307@bymercy.com"
    password = "bopil28307@bymercy.com"

    # url course
    url_course =  "https://netzun.com/mis-contenidos/cursos/261/1264/4346"
    url_course = "https://netzun.com/mis-contenidos/cursos/47/237/984"

    
    ntz = Netzun(email, password, url_course)
    ntz.login()
    ntz.get_table_of_content()
    ntz.add_content_vimeo_url()
    ntz.logout()


#    with open('table_of_content.json','r') as file:
#        table_of_content = json.load(file)
#
#    dl = NetzunDL(table_of_content = table_of_content)
#    dl.dl_course(quality='worst')

  
#    sleep(100)