from tornado import web
import yaml
import CommonMark as cm
from glob import glob


class PageCreator(object):
    def __init__(self, mdfile):
        self.mdfile = mdfile
        self.preamble = '<html><head><link rel="stylesheet" href="tufte.css"/></head><body>'
        self.closing = '</body></html>'

    def __parse_yaml_frontmatter(self, content):
        # Remove a yaml header from the tip of the file, if it exists
        if content[0][:3] == '---':
            for line in content[1:]:
                content.remove(line)
                if line[:3] == '---':
                    break

        return content

    def generate_html(self, mdfile=None):
        if mdfile is None:
            mdf = self.mdfile
        else:
            mdf = mdfile

        filepath = "posts/" + mdf
        if mdf[-3:] != ".md":
            filepath += ".md"

        with open(filepath) as open_md:
            content = open_md.readlines()
            header = []
            markdown = self.__parse_yaml_frontmatter(content)
            markdown = ''.join(markdown)

        return self.preamble + cm.commonmark(markdown) + self.closing


class MetadataPageCreator(PageCreator):

    def __init__(self,mdfile):
        PageCreator.__init__(self,mdfile)
        self.frontmatter = []

    def __parse_yaml_frontmatter(self, content):
        if content[0][:3] == '---':
            for line in content[1:]:
                content.remove(line)
                self.frontmatter += line
                if line[:3] == '---':
                    break
                else:
                    header += line

        return content

def extract_metadata(path):
    metadata = []
    with open(path, 'r') as page:
        content = page.readlines()
        if content[0][:3] == '---':
            for line in content[1:]:
                content.remove(line)
                if line[:3] == '---':
                    break
                else:
                    metadata += line
    if metadata == []: return None
    metadata = ''.join(metadata)
    return yaml.load(metadata)


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
        metadata = {}
        ordered_posts = {}
        if len(posts) > 0:
            for post in posts:
                metadata[post] = extract_metadata(post)
            for post in posts:
                print(metadata[post])
                if metadata[post] is not None:
                    if 'post_number' in metadata[post].keys():
                        ordered_posts[metadata[post]['post_number']] = post[6:-3]
            for i in range(1,len(ordered_posts.keys())+1):
                post = ordered_posts[i]
                archive_content += "1. [" + post + "](" + post + ")\n"

        archive_content += "\n\n"

        print(ordered_posts)

        output += cm.commonmark(archive_content)

        output += '</body></html>'
        self.write(output)
