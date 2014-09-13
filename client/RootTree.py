"""
Description:

Author:
    Neil C

Usage:
    python [filename]

Python Version:
    2.7.5 

Notes:

"""
#==============================================================================
import requests
import ast
import subprocess
import sys
import StringIO
import contextlib
from threading import Thread

SITE_POLL_URL = ''

def poll_site(user, password):
    try:
        r = requests.get(SITE_POLL_URL, auth=(user, password))
    except:
        return None

    return (r.status_code, r.text)

def parse_dicts(string_dict_list_string):
    return ast.literal_eval(string_dict_list_string) 
    
def thread_handle(ex_dict):
    if ex_dict['language'] == 'bash':
        bash_handle(ex_dict)
    elif ex_dict['language'] == 'python':
        python_handle(ex_dict)

def bash_handle(ex_dict):
    code = ex_dict['code']
    p = subprocess.Popen(code, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return (out, err)[0] #TODO Might remove the index

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old    


def python_handle(ex_dict):
    code = ex_dict['code']
    with stdoutIO() as s:
        exec code
    return s.getvalue()

        


if __name__ == '__main__':
    pass
    

    
