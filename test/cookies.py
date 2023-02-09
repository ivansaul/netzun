session = requests.Session()

response = session.post(login_url, data=data)
cookies = response.cookies

source = response.text
iframes = source.find("iframe")

#iframe_response = requests.get("https://player.vimeo.com/video/503726775?h=7b6a8f91c7&app_id=122963")
iframe_response = requests.get("https://player.vimeo.com/video/")
cookies.update(iframe_response.cookies)

iframe_response = requests.get("https://www.googletagmanager.com/ns.html?id=GTM-WXV3NX2&")
cookies.update(iframe_response.cookies)


# Imprimir todas las cookies
for cookie in cookies:
    print(cookie)


