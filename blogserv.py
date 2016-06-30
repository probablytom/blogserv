from tornado import ioloop, web
from handlers import MainHandler, TufteDeliverer, ArchiveHandler
from handlers import FontDeliverer, MarkdownRenderingHandler
import simplenote
import os.path
import asyncio

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
        (r'/([a-zA-Z\-\_]+\.md)', MarkdownRenderingHandler), 
        (r'/([a-zA-Z\-\_]+)', MarkdownRenderingHandler), 
        ])

async def simplenote_update():
    print('Getting new posts')
    # Update posts with simplenote objects
    sn = simplenote.Simplenote(username, password)
    notes = sn.get_note_list(tags=['blogserve_post'])
    if notes[1] is not 0: 
        raise Exception
    else:
        notes = notes[0]
    
    # Get content from the posts found
    for note in notes:
        ret_note = sn.get_note(note['key'])[0]
        note_title = ret_note['content'].split('\n\n')[0]
        note_title = str.replace(note_title, ' ', '_')
        print(note_title) 
        note_content = '\n\n'.join(ret_note['content'].split('\n\n')[1:])

        # post placement
        path = 'posts/' + note_title + '.md'
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'w+') as post_file:
            post_file.write(note_content)
    
    await asyncio.sleep(15)

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    ioloop.IOLoop.instance().add_callback(simplenote_update)
    ioloop.IOLoop.current().start()

