from html.parser import HTMLParser
from pathlib import Path, PureWindowsPath

# <video width="400" controls>
#   <source src="../170elum7dfhqq.mp4" type="video/mp4"/>
#   Your browser does not support HTML5 video.
# </video>

class MyHTMLParser(HTMLParser):
    def __init__(self, filePath, imagesRoot):
        HTMLParser.__init__(self)
        self.content = ''
        self.filePath = filePath
        self.imagesRoot = imagesRoot

    def getContent(self):
        return self.content

    def findFile(self, path, filename):
        for f in Path(PureWindowsPath(path.replace('\\','/'))).rglob(filename):
            return Path(f).as_uri()

    def tranformImagePath(self, path):
        if not path.startswith('../Photos'):
            return path
        path_parts=path.split('/')
        filename=path_parts[len(path_parts)-1]
        return self.findFile(self.imagesRoot, filename)

    def attrsToString(self, attrs = []):
        str = '';
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            if key in ('href','src'):
                value=self.tranformImagePath(value)
            value = '="{0}"'.format(value) if value else ''
            str += '{0}{1} '.format(key, value)
        return str.strip();

    def handle_starttag(self, tag, attrs):
        attrs_str=self.attrsToString(attrs);
        attrs_str = ' ' + attrs_str if len(attrs_str) > 0 else ''
        self.content += "<{0}{1}>".format(tag, attrs_str)

    def handle_endtag(self, tag):
        self.content += '</{0}>'.format(tag)

    def handle_data(self, data):
        self.content += data

