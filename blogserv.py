from tornado import ioloop, web
from handlers import MainHandler, TufteDeliverer, ArchiveHandler
from handlers import FontDeliverer, MarkdownRenderingHandler

def make_app():
    return web.Application([
        (r'/', ArchiveHandler),
        (r'/tufte.css', TufteDeliverer),
        (r'/archive', ArchiveHandler),
        (r'/et-book/([a-zA-Z/.-]*)', FontDeliverer),
        (r'/([a-zA-Z\-\_]+\.md)', MarkdownRenderingHandler), 
        (r'/([a-zA-Z\-\_]+)', MarkdownRenderingHandler), 
        ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    ioloop.IOLoop.current().start()

