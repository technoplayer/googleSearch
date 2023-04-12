import requests
from bs4 import BeautifulSoup


def google_search(search_criteria):
    with requests.Session() as s:
        url = f"https://www.google.com/search?q={search_criteria}"
        headers = {
            "referer": "referer: https://www.google.com/",
            "user-agent": "Mozilla/5.0 (X11; Linux; rv:111.0.1) Gecko/20100101 Firefox/111.0.1"
        }
        s.post(url, headers=headers)
        response = s.get(url, headers=headers)
        return BeautifulSoup(response.text, 'html.parser')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    soup = google_search('pink banana')
    # r1 = soup.find_all("h3")
    allData = soup.find_all("div", {"class": "g"})

    g = 0
    Data = []
    l = {}
    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if link is not None:
            if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                g += 1
                l["link"] = link
                try:
                    l["title"] = allData[i].find('h3').text
                except:
                    l["title"] = None

                try:
                    l["description"] = allData[i].find("span", {"class": "aCOpRe"}).text
                except:
                    l["description"] = None

                l["position"] = g

                Data.append(l)

                l = {}

            else:
                continue

        else:
            continue

        print(Data)

    # print(soup.prettify())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
