import os
import re
import sys
import json
import requests
from tqdm import tqdm
from time import sleep
from pprint import pprint
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, concatenate_audioclips

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        
    def make_podcast(self, file_name, src='videos', dest='videos'):
        """
        Crea un archivo mp3 unificado a partir de los videos descargados del curso
        """

        videos = os.listdir(src)
        videos.sort()
        videos = [v for v in videos if v.endswith('.mp4')]
        videos = [f'{src}/{v}' for v in videos]
        audio = [VideoFileClip(v).audio for v in videos]
        audio = concatenate_audioclips(audio)
        audio.write_audiofile(f"{dest}/{file_name}.mp3")


    def dl_course(self, quality = 'best', dest = 'videos'):
        """
        Download all course videos(presentacion + capsulas)
        """

        # Presentation
        mp4_url = self.get_mp4_url_from_vimeo(self.table_of_content['url_vimeo_presentation'], quality = quality)
        self.mp4_downloader(f'Módulo 0 - Presentación del curso. {self.table_of_content["course_name"]}', mp4_url, dest=dest)

        # Modules
        for k, i in enumerate(self.table_of_content['modules']):
            for j in i['capsulas']:
                filename = f"Módulo {k+1} - {j['cap_titulo']}"
                mp4_url = self.get_mp4_url_from_vimeo(j['url_vimeo'], quality = quality)
                self.mp4_downloader(filename= filename, url=mp4_url, dest=dest)


    def get_mp4_url_from_vimeo(self, url_vimeo:str , quality = 'best'):
        """
        url_vimeo -> https://player.vimeo.com/video/....
        quality -> best, worst

        1. Hacemos un request a player.vimeo y buscamos todos los mp4
           que se encuentran dentro de "progressive":[mp4] 
           
        2. Ordenamos la lista de diccionarios por quality
        """

        headers = {
            'Referer': 'https://netzun.com/', 
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
            'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.get(url_vimeo, headers=headers)
        response = response.text

        # Busca response la #lista después de la palabra "progressive": [#lista] -> #lista
        mamdh = re.search(r'progressive.*?\[(.*?)\]', response)

        if mamdh:
            result = mamdh.group(1)
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
    def __init__(self, email, password, url_course, browser):
        """
        browser: 'firefox', 'chrome'
        """

        self.email = email
        self.password = password
        self.url_course = url_course
        self.url_login = "https://netzun.com/ingresar"
        self.table_of_content = {}
        self.modules = []
        self.course_name = ""
        self.course_description = ""
        self.url_vimeo_presentation = ""
        self.browser = browser

        # Chrome / firefox options en modo headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument('--headless')
        self.firefox_options.add_argument('--disable-gpu')

    def quit(self):
        self.driver.quit()
    
    def login(self):

        ## initialize the chrome / firefox driver
        if self.browser == 'firefox':
            self.driver = webdriver.Firefox(options=self.firefox_options)
        elif self.browser == 'chrome':
            self.driver = webdriver.Chrome("chromedriver", options=self.chrome_options)
        
        # go to netzun login page
        self.driver.get(self.url_login)
    
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
        
        # got to url_course to get the url_course_private
        self.driver.get(self.url_course)
        self.url_course_private = self.driver.current_url


    def get_source_code(self, url):
        """
        Retorna el codigo fuente de una pagina de netzun a partir de una url
        """
        
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "script")))
        return self.driver.page_source
    

    def get_url_vimeo_presentation(self):
        """
        Obtine la url_vimeo de la presentacion del curso
        """

        if self.browser == 'firefox':
            self.driver = webdriver.Firefox(options=self.firefox_options)
        elif self.browser == 'chrome':
            self.driver = webdriver.Chrome("chromedriver", options=self.chrome_options)

        self.url_vimeo_presentation = self.get_url_vimeo(url=self.url_course)


    def get_modules_content(self):
        """
        Retorna un json que contiene toda la informacion del curso:
        Titulo, Modulo, Tema, url, ....
        """

        html = self.get_source_code(self.url_course_private)
        soup = BeautifulSoup(html, "html.parser")

        # Search course name and course description
        self.course_name = soup.find("div", class_="course-name").text
        self.course_description = soup.find("div", class_="description").text
        print(self.course_name)

        # Search modulos and capsulas and save in modules []
        div_modules = soup.find("div", class_="modules")
        li_modules = div_modules.find_all("li", class_=re.compile("accordion__item"))

        for li in li_modules:
            self.modules.append({
                'titulo': li.find("h3").text,
                'n_cap': li.find("p").text,
                'capsulas': [{'cap_titulo': x.text} for x in li.find_all("div", class_="info")]
            })

        # Crea la url para cada capsula a partir de la url base del curso
        *base_url_course, i, j = self.url_course_private.split('/')
        base_url_course, i, j = '/'.join(base_url_course), int(i), int(j)

        for x in self.modules:
            for y in x['capsulas']:
                y['url'] = base_url_course + f"/{i}/{j}"
                # print(base_url_course + f"/{i}/{j}")
                j =j+1
            i = i+1
        
        # Corrige el titulo de las capsulas "Cápsula 3Importa..." -> "Cápsula 3. Importa..."
        for x in self.modules:
            for y in x['capsulas']:
                y['cap_titulo'] = re.sub(r"(\d+)", r"\1. ", y['cap_titulo'])        


        with open('modules.json','w', encoding='utf-8') as file:
            json.dump(self.modules, file, indent=4, ensure_ascii= False)
        
        print(f"N° Módulos: {len(self.modules)}")


    def write_table_of_content(self):
        """
        Crea un archivo md con la que contiene nombre del curso, descripcion, modulos y capsulas
        """           

        with open('table_of_content.md', 'w') as file:
            file.write(f"# {self.course_name}\n\n")
            file.write(f"{self.course_description}\n\n")

            for md in self.modules:
                file.write(f"## {md['titulo']}\n\n")
                for c in md['capsulas']:
                    file.write(f"- {c['cap_titulo']}\n")
                file.write("\n")
        
        with open('table_of_content.json','w', encoding='utf-8') as file:
            self.table_of_content['course_name'] = self.course_name
            self.table_of_content['course_description'] = self.course_description            
            self.table_of_content['url_course'] = self.url_course
            #self.table_of_content['url_course_public'] = self.url_course_public
            self.table_of_content['url_vimeo_presentation'] =self.url_vimeo_presentation
            self.table_of_content['modules'] =self.modules

            json.dump(self.table_of_content, file, indent=4, ensure_ascii= False)

    
    def add_url_vimeo_to_modules(self):
        """
        Añade la url_vimeo a los capsulas
        """
        i,j = 1, sum([len(x['capsulas']) for x in self.modules])
        for md in self.modules:
            print(md['titulo'])
            for c in md['capsulas']:
                c['url_vimeo'] = self.get_url_vimeo(url=c['url'])
                # imprime el recorrido
                print(f"[{i}/{j}] {c['cap_titulo']}")
                i+=1  

        
        with open('modules.json','w', encoding='utf-8') as file:
            json.dump(self.modules, file, indent=4, ensure_ascii= False)
        
        return self.modules

    def get_url_vimeo(self, url: str):
        """
        Retorna la url del iframe -> player.vimeo.com ....
        a partir de la url de una capsula de un modulo
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
    
    email = input('Enter your e-mail: ')
    password = input('Enter your password:')
    url_course = input("Enter the URL of the course to dowload: ")

    print("\n\n")

    ntz = Netzun(email, password, url_course, browser='firefox')    
    ntz.get_url_vimeo_presentation()
    ntz.quit()

    ntz.login()
    ntz.get_modules_content()
    ntz.add_url_vimeo_to_modules()
    ntz.quit()
    
    ntz.write_table_of_content()

    dl = NetzunDL(table_of_content = ntz.table_of_content)
    dl.dl_course(quality='best')
    dl.make_podcast(file_name= ntz.course_name)