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
    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if link is not None:
            if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                link_item = {}

                g += 1
                link_item["link"] = link
                try:
                    link_item["title"] = allData[i].find('h3').text
                except AttributeError:
                    link_item["title"] = None

                try:
                    link_item["description"] = allData[i].find("span", {"class": "aCOpRe"}).text
                except AttributeError:
                    link_item["description"] = None

                link_item["position"] = g

                Data.append(link_item)

            else:
                continue

        else:
            continue

    for item in Data:
        print(item)

    # print(soup.prettify())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
