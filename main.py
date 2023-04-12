import requests
from bs4 import BeautifulSoup
from bottle import Bottle, static_file, request, run, template


app = Bottle()


def google_search(search_criteria, start_no=0, which_google="https://www.google.co.uk"):
    with requests.Session() as s:
        url = f"{which_google}/search?q={search_criteria}&start={start_no}"
        headers = {
            "referer": "referer: https://www.google.com/",
            "user-agent": "Mozilla/5.0 (X11; Linux; rv:111.0.1) Gecko/20100101 Firefox/111.0.1"
        }
        s.post(url, headers=headers)
        response = s.get(url, headers=headers)
        return BeautifulSoup(response.text, 'html.parser')


def get_results(search_criteria, start_no):
    soup = google_search(search_criteria, start_no)
    all_data = soup.find_all("div", {"class": "g"})

    # print(all_data)
    # exit()

    g = 0
    my_data = []
    for i in range(0, len(all_data)):
        link = all_data[i].find('a').get('href')

        if link is not None:
            if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                link_item = {}

                g += 1
                link_item["link"] = link
                try:
                    link_item["title"] = all_data[i].find('h3').text
                except AttributeError:
                    link_item["title"] = None

                try:
                    link_item["description"] = all_data[i].find("span", {"class": "VuuXrf"}).text
                except AttributeError:
                    link_item["description"] = None

                link_item["position"] = g

                my_data.append(link_item)

            else:
                continue

        else:
            continue

    return my_data


def gather_results(search_criteria, total_no):
    start = 0
    final = []
    while start < total_no:
        r_set = get_results(search_criteria, start)
        final = final + r_set
        start += 10
    return final


@app.route('/')
def index():
    return open('website/index.html').read()


# OUR STATIC FILES

@app.route('/css/<filename>')
def server_static(filename):
    print('CSS Served')
    return static_file(filename, root='website/css')


@app.route('/js/<filename>')
def server_static(filename):
    print('JS Served')
    return static_file(filename, root='website/js')


@app.route('/images/<filename>')
def server_static(filename):
    print('Image Served')
    return static_file(filename, root='website/images')


@app.route('/search')
def index():
    query = request.query['query']
    return template(open('website/search.html').read(), results=gather_results(query, 60))


print('Serving on http://localhost:8080')

run(app, host='localhost', port=8080, reloader=True)