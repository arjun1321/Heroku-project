import cherrypy
import os
from Utility import get_top_10_stocks, search_stocks, store_data_to_redis
from jinja2 import Environment, FileSystemLoader


CUR_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        store_data_to_redis()
        template = env.get_template('index.html')
        data = get_top_10_stocks()
        context = {'stocks': data}
        return  template.render(**context)

    @cherrypy.expose
    def search(self, name=''):
        template = env.get_template('list.html')
        if not bool(name.strip()):
            data = get_top_10_stocks()
        else:
            data = search_stocks(name.upper())
        context = {'stocks': data}
        return template.render(**context)


if __name__ == "__main__":

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000))
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'assets'
        },

    }
    webapp = HelloWorld()
    cherrypy.quickstart(webapp, '/', conf)