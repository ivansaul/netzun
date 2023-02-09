"""
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'es-419,es;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'vuid=pl1461177765.498913883; player=""; __cf_bm=Q45yZVX0idySVg_XYbSqaJTXt6Bh1DJG9sNSi_yVg7Q-1675677634-0-AavikfS+BZZCQJ2vpcBi1NWcUk44WMrqzEx6m5dRgj8CPDmteALfwbVMr1gurnFtBXFZxxByzycz7almAsRCMJo=',
    'Pragma': 'no-cache',
    'Referer': 'https://netzun.com/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}

url = 'https://player.vimeo.com/video/503727684?h=09b69d6e56&app_id=122963'
response = requests.get(url, headers=headers)

with open('vimeo_curl.html', 'wb') as f:
    f.write(response.content)
"""

# No son necesarias todas las cabeceras
import requests

url = 'https://player.vimeo.com/video/503727174?h=f818bd11aa&app_id=122963'
headers = {
    'Referer': 'https://netzun.com/', 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
    'sec-ch-ua-platform': '"Linux"'
}

response = requests.get(url, headers=headers)

with open('mp4.html', 'wb') as f:
    f.write(response.content)
