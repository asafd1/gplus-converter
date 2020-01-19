import os
from pathlib import Path, PureWindowsPath
from htmlParser import MyHTMLParser

HTML_ROOT = os.getenv('HTML_ROOT') if os.getenv('HTML_ROOT') else os.getcwd()
IMG_ROOT = os.getenv('IMG_ROOT') if os.getenv('IMG_ROOT') else os.getcwd()

def processFile(file, imagesRoot):
    lines=[]
    content = ''
    filepath = str(file)
    print("processing: " + filepath)
    with open (filepath, 'r', encoding='utf_8') as myfile:
        lines=myfile.readlines()

    for line in lines:
        content+=line

    parser = MyHTMLParser(filepath, imagesRoot)
    parser.feed(content)
    content=parser.getContent();

    os.rename(filepath, filepath + ".bak")

    result_file = open(filepath, 'w+', encoding='utf_8')
    result_file.write(content)
    result_file.close()

def iterateFiles():
    for f in Path(PureWindowsPath(HTML_ROOT.replace('\\','/'))).rglob('*.html'):
        processFile(f, IMG_ROOT)

iterateFiles()