# cs457-557-fall2020-pa1-Smriti0311

Programming Assignment 1 : Multi-Threaded HTTP Server

Implementation:
1. Using socket programming and multi-threading, this HTTP server has been created.
2. This HTTP server satisfies GET requests. 
3. If a particular file is present, the server returns the HTTP response header, containing a status code 200, date, server name, last-modified date, content-length, content-type, along with that resource to the client
4. Else, server returns a header with status code 404 and an error message to the client.

To run :

1. Open a server terminal on a remote machine, say remote01.cs.binghamton.edu.
2. On this server terminal, put the command : python3 pa1.py
3. Open a client terminal on a remote machine, 
say remote02.cs.binghamton.edu
4. On this client terminal, put the command :
wget http://remote01.cs.binghamton.edu:PORT_NUMBER/resource_name
5. The requested resource will get downloaded on the client machine
6. The server terminal will show the output which contains the resource name, IP address of client, port number of client and access count of that particular resource since the server started.
7. Ctrl-C serves as keyboard interrupt and will shut down the server.
