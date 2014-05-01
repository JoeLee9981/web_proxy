web_proxy
=========

This is a python based web proxy server, designed for caching purpoes.
*It requires Python 2.7 to compile and run.

How it works:
  The server intercepts communication from a standard web browser like firefox and parses the HTTP GET message 
  to obtain the website requested. It will then open a new socket and send a slightly modified GET request.
  It then loads the web page into a cache and returns it to the web browser, then closes both sockets. It makes use
  of a TCP socketed connection using the python select library to function asynchronously.
  
How to compile:
  Using python 2.7 run the main.py module. This will create the server and bind it to your localhost at port 12333.
  To make use of it, edit the configuration of your web browser to use a proxy server at 127.0.0.1 at port 12333, and
  then load web pages as usual.
  
Included is a simple client you can use to test, assuming you don't want to change your web browser configuration. Simply run
the server as per instructions above, then use python 2.7 to run the run_client.py file. This will connect automatically
to your localhost at port 12333. At this point simply type in a GET request like "GET http://www.google.com HTTP/1.0" (excluding
quotation marks) then sit back and watch the communication go!
