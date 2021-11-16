import requests
from bs4 import BeautifulSoup
import codecs
import time
import pandas as pd


cryptocurrency = []

url = 'https://coinmarketcap.com/?page='

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

for x in range(1,5):
    def get_data(url, headers=headers):
        r = requests.get(url+str(x), headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        ''' create/download html to local '''
        #f = open('./res.html', 'wb')
        #f.write(r.content)
        #f.close()

        ''' open/read local html file '''
        file = codecs.open('res.html', 'r', 'utf-8')
        info = file.read()
        #soup = BeautifulSoup(info, 'html.parser')
        return soup


    def parse(soup, cryptocurrency):
        contents = soup.find_all('tr')
        for item in contents:
            try:
                rank = item.find('div', {'class': 'sc-1teo54s-3 etWhyV'}).text.strip()
                logo = item.find('img', {'class': 'coin-logo'})['src']
                title = item.find('p', {'class': 'sc-1eb5slv-0 iworPT'}).text.strip()
                symbol = item.find('p', {'class': 'sc-1eb5slv-0 gGIpIK coin-item-symbol'}).text.strip()
                price = item.find('div', {'class': 'sc-131di3y-0 cLgOOr'}).text.strip()
                pricech24h = item.find('span',{'class': 'sc-15yy2pl-0 hzgCfk'}).text
                marketcap = item.find('span', {'class': 'sc-1ow4cwt-1 ieFnWP'}).text
                volume24h1 = item.find('p', {'class': 'sc-1eb5slv-0 hykWbK font_weight_500'}).text.strip()
                circulatingspply = item.find('p', {'class': 'sc-1eb5slv-0 kZlTnE'}).text.strip()
                fullydilutedmcap = item.find('span', {'class': 'sc-1ow4cwt-1 ieFnWP'}).text

                results = {
                    'rank': rank,
                    'logo': logo,
                    'title': title,
                    'symbol': symbol,
                    'price': price,
                    'price24h': pricech24h,
                    'marketcap': marketcap,
                    'volume24h1': volume24h1,
                    'circulatingspply': circulatingspply,
                    'fullydilutedmcap': fullydilutedmcap,
                }
                cryptocurrency.append(results)
                time.sleep(2)
                print('crypto found: ', len(cryptocurrency))
            except:
                pass
        return cryptocurrency


    def output(cryptocurrency):
        df = pd.DataFrame(cryptocurrency)
        print(df.head(), df.tail())
        df.to_csv('crypto.csv')
        df.to_json('crypto.json')
        return

    soup = get_data(url, headers=headers)
    cryptocurrency = parse(soup, cryptocurrency)
    output(cryptocurrency)
