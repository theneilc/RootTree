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
import random
import struct
from Crypto.Cipher import AES

AUTH_ENC_FILE_NAME = 'auth.enc'
SITE_POLL_URL = ''
SITE_CONFIRM_URL = ''
AWSAccessKeyId = 'AKIAJQE2SYERMZG7CL5Q'

def encrypt_file(key, in_contents, out_filename, chunksize=64*1024):
    """ Encrypts a string using AES (CBC mode) with the given key.

        key:
            The encryption key - a string that must be either 16, 24 or 32 
            bytes long. Longer keys are more secure.

        in_contents:
            String to encrypt and write to file 

        out_filename:
            File where the encrypted data is written to

        chunksize:
            Sets the size of the chunk which the function uses to read and 
            encrypt the file. Larger chunk uses to read and encrypt the file.
            Larger chunk sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = len(in_contents)

    with open(out_filename, 'wb') as outfile:
        outfile.write(struct.pack('<Q', filesize))
        outfile.write(iv)

        chunk = in_contents[:chunksize]
        if len(chunk) == 0:
            return 
        elif len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)

        outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the given key. Parameters are
        similar to encrypt_file, with one difference: in_filename is the input
        file that is to be decrypted. The decrypted string is returned.
    """

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            return ''
        return str(decryptor.decrypt(chunk))[:origsize]
    
def get_key():
    """ Returns the secret key used in the AES encryption of the files in the
        Encryption module
    """
    SECRET_KEY_AES = 'e88a0fd7bc19496aba7f80f522c29722'
    return SECRET_KEY_AES

def get_credentials_from_file():
    """ Returns the credentials created by this module's main method in a list
    """
    decrypted_auth = decrypt_file(get_key(), AUTH_ENC_FILE_NAME)
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
    
    encrypt_file(get_key(), username + ',' + password,
                         AUTH_ENC_FILE_NAME)



def poll_site(user, password):
    try:
        r = requests.get(SITE_POLL_URL, auth=(user, password))
    except:
        return None

    return (r.status_code, r.text)

def parse_dicts(string_dict_list_string):
    return ast.literal_eval(string_dict_list_string) 
    
def thread_handle(ex_dict, username, password):
    if ex_dict['language'] == 'bash':
        output = bash_handle(ex_dict)
    elif ex_dict['language'] == 'python':
        output = python_handle(ex_dict)

    if ex_dict['file_path'] != True:
        u_params = upload_file(ex_dict['policy'], ex_dict['signature'],\
                               ex_dict['uuid'], filepath=ex_dict['file_path'])
    else:
        u_params = upload_file(ex_dict['policy'], ex_dict['signature'],\
                               ex_dict['uuid'], content=output)

    client_confirm(ex_dict['uuid'], u_parms, username, password)

def client_confirm(uuid, param_dict, username, password):
    v1 = {}
    v1.update(param_dict)
    v1['uuid'] = uuid
    requests.post(SITE_CONFIRM_URL, data=v1, auth=(username, password))


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

def upload_file(policy, signature, uuid, filepath=None, content=None):
    url = 'https://roottreebucket.s3.amazonaws.com/'
    payload = {
                'key': '${filename}',
                'AWSAccessKeyId': 'AKIAJQE2SYERMZG7CL5Q',
                'acl': 'public-read',
                'policy': policy,
                'signature': signature,
               }

    url_list = {}
    #rename the file, and open it
    if filepath is not None:
        base = os.path.basename(filepath)
        original_filename = os.path.splitext(base)[0]
        extension = os.path.splitext(base)[1]
        directory = os.path.dirname(filepath)
        new_filepath = directory + '/' + uuid + extension
        os.rename(filepath, new_filepath)
        files_temp = open(new_filepath, 'r')
        files = {'file': files_temp}
        r = requests.post(url, data=payload, files=files)
        os.rename(new_filepath, filepath)
        files_temp.close()
        url_list['file_url'] = r.headers['location']

    if content is not None:
        print content
        metafile_name = uuid + '_meta.txt'
        metafile = open(metafile_name, 'w')
        metafile.write(content)
        metafile.close()
        metafile = open(metafile_name, 'r')
        files = {'file': metafile}
        r = requests.post(url, data=payload, files=files)
        metafile.close()
        url_list['result_url'] = r.headers['location']
    
    return url_list


if __name__ == '__main__':
    # TODO INITIALIZE

    if os.path.isfile(AUTH_ENC_FILE_NAME) != True:
        auth_main()

    credentials = get_credentials_from_file()
    username = credentials[0]
    password = credentials[1]
    


    while True:
        #TODO get credentials
        site_polled = poll_site(username, password)
        
        command_dicts = parse_dicts(site_polled[1])

        for command_dict in command_dicts:
            t = Thread(target=thread_handle, args=(command_dict, username,\
                                                   password ))
            t.daemon = True
            t.start()

    

    
