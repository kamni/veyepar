# youtube_uploader.py 
# youtbe specific code

# caled from post_yt.py 
# which someday will be jsut post.py with a yt parameter.

# http://code.google.com/apis/youtube/1.0/developers_guide_python.html
# http://code.google.com/apis/youtube/2.0/reference.html

import gdata.media
import gdata.geo
import gdata.youtube
import gdata.youtube.service

from gdata.youtube.service import YouTubeError

import pw

def progress(self, current, blocksize, total):
    """
    Displaies upload percent done, bytes sent, total bytes.
    """
    elapsed = datetime.datetime.now() - self.start_time 
    remaining_bytes = total-current
    if elapsed.seconds: 
        bps = current/elapsed.seconds
        remaining_seconds = remaining_bytes / bps 
        eta = datetime.datetime.now() + datetime.timedelta(seconds=remaining_seconds)
        sys.stdout.write('\r%3i%%  %s of %s MB, %s KB/s, elap/remain: %s/%s, eta: %s' 
          % (100*current/total, current/(1024**2), total/(1024**2), bps/1024, stot(elapsed.seconds), stot(remaining_seconds), eta.strftime('%H:%M:%S')))
    else:
        sys.stdout.write('\r%3i%%  %s of %s bytes: remaining: %s'
          % (100*current/total, current, total, remaining_bytes, ))


class ProgressFile(file):
    def __init__(self, cb, *args, **kw):
        self.cb = cb
        file(self, *args, **kw)

    def read(self, size=-1):
        try:
            self.cb(self.tell(), size, self.size())
            return file.read(self, size)
        finally:
            self.cb(self.tell(), size, self.size())

class Uploader(object):

    # input attributes:
    files = []
    thumb = ''
    meta = {}
    upload_user = ''
    old_url = ''
    user=''
    private=False

    # return attributes:
    ret_text = ''
    new_url = ''

    def auth(self):
         
        yt_service = gdata.youtube.service.YouTubeService()
        gauth = pw.yt[self.user]

        yt_service.email = gauth['email']
        yt_service.password = gauth['password']
        yt_service.source = 'video eyebaal review'
        yt_service.developer_key = gauth['dev_key']
        yt_service.client_id = self.user

        yt_service.ProgrammaticLogin()

        return yt_service
       
    def media_group(self):
        # prepare a media group object to hold our video's meta-data
        media_group = gdata.media.Group(
            title=gdata.media.Title(
                text=self.meta['title']),
            description=gdata.media.Description(
                description_type='plain',
                text=self.meta['description']),
            keywords=gdata.media.Keywords(
                text=','.join(self.meta['tags'] )),
            category=[gdata.media.Category(
                # label=self.meta['category'],
                # text=self.meta['category'],
                label="Education",
                text="Education",
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                )],
            player=None
            )
        if self.meta['hidden']:
            media_group.private=gdata.media.Private()

        return media_group


    def geo(self):
        # prepare a geo.where object to hold the geographical location
        # of where the video was recorded
        where = gdata.geo.Where()
        # where.set_location((37.0,-122.0))
        where.set_location(self.meta['latlon'])

        return where

 
    def upload(self):

        yt_service = self.auth()

        video_entry = gdata.youtube.YouTubeVideoEntry(
                media=self.media_group())

        if self.meta.has_key('latlon'):
            video_entry.geo = self.geo()

        # add some more metadata -  more tags
        print self.meta['tags']
        video_entry.AddDeveloperTags(self.meta['tags'])

        # actually upload
        pathname= self.files[0]['pathname']
        print pathname
        pf = ProgressFile(progress,pathname,'r')
        try:
            # self.new_entry = yt_service.InsertVideoEntry(video_entry, pathname)
            self.new_entry = yt_service.InsertVideoEntry(video_entry, pf)
            self.ret_text = self.new_entry.__str__()
            link = self.new_entry.GetHtmlLink()
            self.new_url = link.href.split('&')[0]
            ret = True

        except gdata.youtube.service.YouTubeError as e:
            import code
            code.interact(local=locals())
            self.ret_text = e.__str__()
            ret = False

        return ret
    
    def extra_stuff(self):

        upload_status = yt_service.CheckUploadStatus(new_entry)

        if upload_status is not None:
            video_upload_state = upload_status[0]
            detailed_message = upload_status[1]

            print video_upload_state
            print detailed_message

        entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
        print 'Video flash player URL: %s' % entry.GetSwfUrl()

        # show alternate formats
        for alternate_format in entry.media.content:
            if 'isDefault' not in alternate_format.extension_attributes:
              print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                         alternate_format.url)

        # show thumbnails
        for thumbnail in entry.media.thumbnail:
            print 'Thumbnail url: %s' % thumbnail.url

if __name__ == '__main__':
    u = Uploader()
    u.meta = {
     'title': "test title",
     'description': "test description",
     'tags': ['tag1', 'tag2'],
     'category': "Education",
     'hidden': 0,
     'latlon': (37.0,-122.0)
    }

    u.files = ['/home/carl/Videos/veyepar/test_client/test_show/mp4/Test_Episode.mp4']
    u.user = 'ndv'

    ret = u.upload()

    print "print u.new_entry.id.text"

    import code
    code.interact(local=locals())
    # import pdb
    # pdb.set_trace()



