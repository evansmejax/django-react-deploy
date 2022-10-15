
import time
from pathlib import Path
import os
import codecs
import shutil
import subprocess

def updateSettings(inputf,mapping):
    #read input file
    fin = open(inputf, "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    for k,v in mapping.items():
        data = data.replace(k, v)
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(inputf, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

frontend = "frontend"
backend = "backend"
settings = "backend/core/settings.py"

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
    static_in = normalizePath(os.path.join(BASE_DIR,f'{frontend}/build/static'))
    static_out = normalizePath(os.path.join(BASE_DIR,f'{backend}/static'))

    # delete everything in static out
    if os.path.isdir(static_out):
        shutil.rmtree(static_out)
        shutil.copytree(static_in, static_out)
    
    
    updateSettings(settings,{
        'DEBUG = True': 'DEBUG = False', 
    })
    
    temp = 'backend_b'

    shutil.copytree(backend , temp ,ignore=shutil.ignore_patterns(".git",'media'))
    shutil.make_archive('output', 'zip', temp)
    shutil.rmtree(temp)
    
    updateSettings(settings,{
        'DEBUG = False': 'DEBUG = True', 
    })

if __name__ == '__main__':
    start_time = time.time()
    task()
    seconds_taken = time.time() - start_time
    print("--- program excecuted in %s seconds ---" % seconds_taken)