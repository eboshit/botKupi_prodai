import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
def pars(count):
    list_url = ['']
    id = 0
    while len(list_url) <= count:
        id += 1
        url = f'https://msk.kupiprodai.ru/lichnoe/moscow_odezhdamuzhskaya/page{id}/'
        response = requests.get(url)
        if response.status_code == 200 or response.status_code == '200':
            print(url)
            response = response.text
            html = bs(response, 'html.parser')
            n_f = str(html.select('li', class_="list_title"))
            data = n_f.split(' ')
            for i in data:
                if 'href' in i:
                    url = i.split('href="')
                    if len(url) > 1:
                        url = url[1].split('"')
                        url = url[0]
                        if 'https://msk.kupiprodai.ru/' in url:
                            if url not in list_url:
                                list_url.append(url)
                        if len(list_url) == count:
                            break

        else:
            for i in list_url:
                print(i)
            break
    for i in list_url:
        print(i)
    print(len(list_url))
    print(list_url[3])

    """#allNews = soup.findAll('ul', class_='width100 list margin_bottom_20')
    for i in data:
        s = i.split('"')
        if 'https://msk.kupiprodai.ru/' in s[0] :
            filteredNews.append(s[0])
    #class ="width100 list margin_bottom_20"
    #print(filteredNews)"""
pars(200)

