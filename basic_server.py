from tornado import ioloop, web
import CommonMark as cm
from glob import glob

class PageCreator(object):
    def __init__(self, mdfile):
        self.mdfile = mdfile
        self.preamble = '<html><head><link rel="stylesheet" href="tufte.css"/></head><body>'
        self.closing = '</body></html>'

    def generate_html(self, mdfile=None):
        if mdfile is None:
            mdf = self.mdfile
        else:
            mdf = mdfile

        markdown = ""
        filepath = "posts/" + mdf
        if mdf[-3:] != ".md":
            filepath += ".md"

        with open(filepath) as open_md:
            markdown += open_md.read()

        return self.preamble + cm.commonmark(markdown) + self.closing

class MainHandler(web.RequestHandler):
    def get(self):
        parser = PageCreator('index.md')
        with open('index.md') as open_md:
            self.write(parser.preamble + cm.commonmark(open_md.read()) + parser.closing)

class MarkdownRenderingHandler(web.RequestHandler):
    def get(self, postname):
        parser = PageCreator(postname)
        self.write(parser.generate_html())

class TufteDeliverer(web.RequestHandler):
    def get(self):
        with open('tufte.css') as tufte:
            self.write(tufte.read())

class FontDeliverer(web.RequestHandler):
    def get(self, path):
        with open('et-book/'+path) as font_file:
            self.write(font_file.read())

class ArchiveHandler(web.RequestHandler):
    def get(self):
        posts = glob("posts/*.md")
        output = '<html><head><link rel="stylesheet" href="tufte.css"/></head><body>'

        archive_content = "# Archive\n\nHere's an archive of all of my published posts:\n\n"
        if len(posts) > 0:
            posts = [post[6:-3] for post in posts] # Strip file extensions and path from titles of posts
            for post in posts:
                archive_content += "* [" + post + "](" + post + ")\n"

        archive_content += "\n\n"

        output += cm.commonmark(archive_content)

        output += '</body></html>'
        self.write(output)


def make_app():
    return web.Application([
        (r'/', MainHandler),
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

