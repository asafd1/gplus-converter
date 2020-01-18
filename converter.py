from html.parser import HTMLParser
from pathlib import Path, PureWindowsPath
import os


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content=''

    def getContent(self):
        return self.content

    def findFile(self, path, filename):
        for f in Path(PureWindowsPath(path.replace('\\','/'))).rglob(filename):
            print(Path(f).as_uri())
            return f

    def tranformImagePath(self, path):
        if not path.startswith('../Photos'):
            return path
        path_parts=path.split('/')
        filename=path_parts[len(path_parts)-1]
        self.findFile(PATH, filename)
        print(filename)
        return path

    def toString(self, attrs = []):
        str = '';
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            if key=='href':
                value=self.tranformImagePath(value)
            value = '="{0}"'.format(value) if value else ''
            str += '{0}{1} '.format(key, value)
        return str.strip();

    def handle_starttag(self, tag, attrs):
        attrs_str=self.toString(attrs);
        attrs_str = ' ' + attrs_str if len(attrs_str) > 0 else ''
        self.content += "<{0}{1}>".format(tag, attrs_str)

    def handle_endtag(self, tag):
        self.content += '</{0}>'.format(tag)

    def handle_data(self, data):
        self.content += data

lines=[]
content=''
with open ('example.html', 'r', encoding='utf_8') as myfile:
    lines=myfile.readlines()

for line in lines:
    content+=line

parser = MyHTMLParser()
parser.feed(content)
content=parser.getContent();

result_file = open('result.html', 'w+', encoding='utf_8')
result_file.write(content)
result_file.close()