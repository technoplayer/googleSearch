from bottle import Bottle, static_file, request, run, template

app = Bottle()


# OUR HOMEPAGE

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
    return template(open('website/search.html').read(), results=search(query))


# RUNNING OUR SERVER

print('Serving on http://localhost:8080')

run(app, host='localhost', port=8080, reloader=True)
