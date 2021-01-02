#!/usr/bin/env python3

from socket import *
import sys
import os
import mimetypes
import time 
from wsgiref.handlers import format_date_time
import datetime
import threading


# Creates a dictionary to track access count of each resource
def create_dict():
        global rsrc
        if 'rsrc' not in globals():
                rsrc = {}

# increments access count
def is_accessed(file_name):
        if file_name in rsrc:
                rsrc[file_name] +=1 
        else:
                rsrc[file_name] = 1


# creates the header for response
def create_header(full_path):
        mtype = mimetypes.MimeTypes().guess_type(full_path)
        var5 = open(full_path, 'rb')
        var6 = var5.read()
        h1 = 'HTTP/1.1 200 OK' + '\n'
        h2 = 'Date:' + str(format_date_time(time.time())) + '\n'
        h3 = 'Server: Apache' + '\n'
        var7 = os.stat(full_path)
        var8 = var7.st_mtime
        var9 = datetime.datetime.fromtimestamp(var8).strftime('%a, %d %b %Y %H:%M:%S GMT') 
        var10 = os.path.getsize(full_path)
        h4 = 'Last-Modified: ' + str(var9) + '\n'
        h5 = 'Content-Length: ' + str(var10) + '\n'
        h6 = 'Content-Type: ' + str(mtype) + '\n'
        h7 = 'Connection: close' + '\n'
        h8 =  '\r\n'
        header = ''.join((h1, h2, h3, h4, h5, h6, h7, h8))
        return header


# serves GET request by a client
def clt_thread(clt, address):
        try:
                clt_data = clt.recv(1024).decode('utf-8')
                if not clt_data:
                        sys.exit('No data from client')
                
                # extract the filename from the client request
                var1 = clt_data.split('\n')
                var2 = var1[0].split(' ')
                var3 = str(var2[1])
                var4 = os.getcwd() + '/www' + str(var2[1])

                # if resource is present, with header, encode it, and send it to client
                if os.path.isfile(var4):
                        is_accessed(var3)
                        var5 = open(var4, 'rb')
                        var6 = var5.read()
                        header = create_header(var4)
                        header = header.encode('utf-8')
                        response = header + var6
                        clt.sendall(response)
                        print(str(var3) + '|' + str(address[0]) + '|' + str(address[1]) + '|' + str(rsrc[var3]) )
                        clt.close()
                
                # else exit with error code 404
                else:
                        v1 = 'HTTP/1.1 404 FILE NOT FOUND'+'\n'
                        v2 = 'Connection: close' + '\n'
                        v3 = '\r\n'
                        header = ''.join((v1, v2, v3))
                        clt.sendall(header.encode('utf-8'))
                        clt.close()
                        sys.exit('Error 404 File not found') 


        except Exception as e:
                print('\n\t', e, '\n')
                
                

                                        
# this function creates a server that runs infinitely unless stopped by keyboard interrup or other exception                                                          
def create_Server():
        try:
                while True:
                        s = socket(AF_INET, SOCK_STREAM)
                        s.bind((gethostname(), 0))
                        print('\t\t ---------- \t\t')
                        
                        s.listen()
                        print('Server running on http:{0}:{1}'.format(gethostbyname(gethostname()), s.getsockname()[1]))
                        path = os.getcwd()
                        path1 = path + '/www'
                        isdir = os.path.isdir(path)

                        if not isdir:
                                sys.exit('The www directory does not exist.')

                        clt, address = s.accept()
                        print('Connected to ' + address[0] +' | '+ str(address[1]))

                        my_thread = threading.Thread(target=clt_thread, args=(clt, address, ))
                        my_thread.start()
                        
                                                
        except KeyboardInterrupt:
                print('\tA keyboard interrupt was entered')
        except Exception as e:
                print('\n\t', e, '\n')


create_dict()
create_Server()
