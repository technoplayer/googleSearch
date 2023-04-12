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
    soup = google_search('cisco')

    # title = soup.select(".DKV0Md span")
    #
    # for t in title:
    #     print(f"Title: {t.get_text()}\n")

    print(soup.prettify())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
