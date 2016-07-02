import simplenote
import os.path
import asyncio

async def simplenote_update():
    notes = get_posts()
    process_notes(notes)
    
    await asyncio.sleep(15)

def get_posts():
    # Update posts with simplenote objects
    sn = simplenote.Simplenote(username, password)
    notes = sn.get_note_list(tags=['blogserve_post'])
    if notes[1] is not 0: 
        raise Exception
    else:
        notes = notes[0]

    return notes

# TODO: Error handling
def process_posts(notes):
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
    
username, password = '',''
with open('simplenote_credentials.txt', 'r') as auth:
    creds = auth.readlines()
    username, password = creds[0][:-1], creds[1][:-1]

