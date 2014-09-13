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
import StringIO
import contextlib
from threading import Thread
import sys
import os
from Tkinter import *
from datetime import datetime

AUTH_ENC_FILE_NAME = 'auth.enc'
SITE_POLL_URL = ''

def get_key():
    """ Returns the secret key used in the AES encryption of the files in the
        Encryption module
    """
    SECRET_KEY_AES = 'e88a0fd7bc19496aba7f80f522c29722'
    return SECRET_KEY_AES

def get_credentials_from_file():
    """ Returns the credentials created by this module's main method in a list
    """
    decrypted_auth = encrypt.decrypt_file(get_key(), AUTH_ENC_FILE_NAME)
    return decrypted_auth.split(',')

def getpwd(errorflag=0):
    """ Prompts the running Python process with a Tkinter GUI for confirming
        the input username and password with Dentboard
    """
    credentials = []
    root = Tk()
    usrbox = Entry(root)
    pwdbox = Entry(root, show = '*')
    def onpwdentry(evt):
        credentials.append(usrbox.get())
        credentials.append(pwdbox.get())
        root.destroy()
    def onokclick():
        credentials.append(usrbox.get())
        credentials.append(pwdbox.get())
        root.destroy()


    if errorflag != 0:
        if errorflag == 1:
            Label(root, text = "Your username or password were incorrect") \
                 .pack(side='top')

    Label(root, text = 'TheDentboard Username').pack(side = 'top')
    usrbox.pack(side = 'top')

    Label(root, text = 'Password').pack(side = 'top')
    pwdbox.pack(side = 'top')

    Button(root, command=onokclick, text = 'OK').pack(side = 'top')

    root.mainloop()
    return credentials

def auth_main():
    credentials = getpwd()
    username = credentials[0]
    password = credentials[1]
    
    #TODO MODIFY
    while upload.test_credentials(username, password) == 0:
        credentials = getpwd(1)
        username = credentials[0]
        password = credentials[1]

    encrypt.encrypt_file(get_key(), username + ',' + password,
                         AUTH_ENC_FILE_NAME)



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
    stdinput =  ex_dict.get('stdin', '')
    p = subprocess.Popen(code, stdout=subprocess.PIPE, stdin=subprocess.PIPE,\
                         shell=True)
    out, err = p.communicate(input=stdinput)
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
    

    
