from tornado import ioloop, web
from handlers import MainHandler, TufteDeliverer, ArchiveHandler
from handlers import FontDeliverer, ImageDeliverer, MarkdownRenderingHandler
from sn_driver import simplenote_update

username, password = '',''
with open('simplenote_credentials.txt', 'r') as auth:
    creds = auth.readlines()
    username, password = creds[0][:-1], creds[1][:-1]


def make_app():
    return web.Application([
        (r'/', ArchiveHandler),
        (r'/tufte.css', TufteDeliverer),
        (r'/archive', ArchiveHandler),
        (r'/et-book/([a-zA-Z/.-]*)', FontDeliverer),
        (r'/images/([a-zA-Z/.-]*)', ImageDeliverer),
        (r'/([a-zA-Z\-\_]+\.md)', MarkdownRenderingHandler), 
        (r'/([a-zA-Z\-\_]+)', MarkdownRenderingHandler), 
        ])

    
if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    ioloop.IOLoop.instance().add_callback(simplenote_update)
    ioloop.IOLoop.current().start()

