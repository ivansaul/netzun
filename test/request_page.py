import requests

headers = {
  'authority': 'netzun.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'es-419,es;q=0.8',
  'cache-control': 'no-cache',
  'cookie': 'auth.strategy=local; cartData=%5B%5D; _locationData=%7B%22id%22%3A3%2C%22code%22%3A%22US%22%2C%22currency%22%3A%22USD%22%2C%22payment_currency%22%3A%22USD%22%2C%22symbol%22%3A%22US%24%22%7D; campaign=%7B%7D; _hostname=netzun.com; showFreemiumIntro=true; permisionCoockie=true; _gcl_au=1.1.722431215.1675663319; prism_26233020=0853b719-1e7f-4ad8-b6a8-199181eec6b8; _gid=GA1.2.250511934.1675663321; _ym_uid=1675663323825642608; _ym_d=1675663323; ln_or=eyIyODMzMjEwIjoiZCJ9; _ym_isad=1; _fbp=fb.1.1675663331363.891414383; _urlprev=; _ga=GA1.2.1959464846.1675663321; __onboardingProgress=%7B%22preferences%22%3A%5B%22Negocios%22%2C%22Estilo%20de%20vida%22%5D%2C%22phone%22%3A%221%20946782676%22%2C%22first_name%22%3A%22dixey%22%2C%22last_name%22%3A%22dixey%20dixey%22%2C%22birthday%22%3A%221997-07-22%22%2C%22country%22%3A%7B%22flag%22%3A%22https%3A%2F%2Fnetzunplus.s3.amazonaws.com%2Ffrontend-assets%2Fflags%2Fusa.svg%22%2C%22name%22%3A%22Estados%20Unidos%22%2C%22alpha2Code%22%3A%22US%22%2C%22alpha3Code%22%3A%22USA%22%2C%22callingCodes%22%3A%221%22%7D%2C%22gender%22%3A%7B%22value%22%3A%22F%22%2C%22name%22%3A%22Femenino%22%7D%2C%22id_preferences%22%3A%5B26%2C36%5D%7D; _ga_FY1FZ2B9HG=GS1.1.1675663323.1.1.1675668740.28.0.0; _ga_2387651196=GS1.1.1675663324.1.1.1675668740.0.0.0; auth.redirect=%2Fmis-contenidos; auth._token.local=Token%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJuZXR6dW4uY29tIiwic3ViIjoiZGl4ZXkiLCJqdGkiOjcxMTMzNCwiaWF0IjoxNjc1Njk0MzUyLjAsIm5iZiI6MTY3NTY5NDM1Mi4wLCJleHAiOjE3MTE5ODIzNTIuMH0.t72jLFr6a_yBsln-84irnm2kGSC2aAbofFyEs1tvW2k; auth._token_expiration.local=1711982352000; data=%7B%22access_token%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJuZXR6dW4uY29tIiwic3ViIjoiZGl4ZXkiLCJqdGkiOjcxMTMzNCwiaWF0IjoxNjc1Njk0MzUyLjAsIm5iZiI6MTY3NTY5NDM1Mi4wLCJleHAiOjE3MTE5ODIzNTIuMH0.t72jLFr6a_yBsln-84irnm2kGSC2aAbofFyEs1tvW2k%22%2C%22user%22%3A%7B%22first_name%22%3A%22dixey%22%2C%22last_name%22%3A%22dixey%22%7D%7D',
  'pragma': 'no-cache',
  'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'sec-gpc': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

url = 'https://netzun.com/mis-contenidos/cursos/261/1264/4347'

response = requests.get(url, headers=headers)

with open('page_curl.html', 'w') as f:
    f.write(response.text)
