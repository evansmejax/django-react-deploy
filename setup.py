
import time
from pathlib import Path
import os
import codecs
import shutil
import subprocess

frontend = "frontend"
backend = "backend"

def normalizePath(path):
    return os.path.normpath(path).replace(os.sep, "/")

def task():
    BASE_DIR = Path(__file__).resolve().parent
    # delete build folder
    build_folder = normalizePath(os.path.join(BASE_DIR,f'{frontend}/build'))
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder)
    # build npm
    subprocess.check_call(f'npm run build --prefix {frontend}', shell=True)
    # move index file
    index_in = normalizePath(os.path.join(BASE_DIR,f'{frontend}/build/index.html'))
    index_out = normalizePath(os.path.join(BASE_DIR,f'{backend}/templates/index.html'))
    static_in = normalizePath(os.path.join(BASE_DIR,f'{frontend}/build/static'))
    static_out = normalizePath(os.path.join(BASE_DIR,f'{backend}/static'))
    if os.path.isfile(index_in):
        file = codecs.open(index_in, "r", "utf-8")
        html = file.read()
        # uncomment this block if you have django-seo-ok package
        html_pieces = html.split('<head>')
        html_pieces = [html_pieces[0],'{% load seo %}','<head>','{% get_seo_data request.seo %}',html_pieces[1]]
        html_updated = ''.join(html_pieces)
        html = html_updated
        f = open(index_out, 'w')
        f.write(html)
        f.close()

    # delete media files
    media = normalizePath(os.path.join(BASE_DIR,f'{backend}/media'))
    shutil.rmtree(media)
    os.mkdir(media)

    # delete everything in static out
    if os.path.isdir(static_out):
        shutil.rmtree(static_out)
        shutil.copytree(static_in, static_out)
    temp = 'backend_b'
    shutil.copytree(backend , temp ,ignore=shutil.ignore_patterns(".git"))
    shutil.make_archive('output', 'zip', temp)
    shutil.rmtree(temp)

if __name__ == '__main__':
    start_time = time.time()
    task()
    seconds_taken = time.time() - start_time
    print("--- program excecuted in %s seconds ---" % seconds_taken)