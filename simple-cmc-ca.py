#!/usr/bin/python

import sys, getopt
import os, cgi, SimpleHTTPServer, SocketServer, logging
import subprocess

PORT = 8000
POST = False


def usage():
  print 'Simple Python HTTP Server'
  print 'Usage [OPTION]\n'
  print '   -p, --port                      Set the port to listen on (default is 8080)'
  print '     , --post <ON/OFF>             Allow Post (Default is OFF; will not overwrite existing file)'
  print ''


class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning(" =========================================================")
        logging.warning(" =======================    GET   ========================")
        logging.warning(self)
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        logging.warning(" ======================= Get Done ========================")
        logging.warning(" =========================================================")


class GetHandlerWithPOST(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning(" =========================================================")
        logging.warning(" =======================    GET   ========================")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        logging.warning(" ======================= Get Done ========================")
        logging.warning(" =========================================================")

     def do_POST(self):
        if(POST):
           logging.warning(" =========================================================")
           logging.warning(" =======================    POST  ========================")
           logging.warning(self.headers)


           # Check if path is there.
           if self.path:

               # Get length of the data and read it.
               length = self.headers['content-length']
               data = self.rfile.read(int(length))

               if(self.path == "/simple.csr"):
                  # Write the data to a file in current dir.
                  with open(os.getcwd() + self.path, 'wb') as file:
                      logging.warning("201: Creating File [" + str(os.getcwd() + self.path) + "]")
                      file.write(data)
                  subprocess.call(["certify.sh"])
                  self.send_response(200)
                  self.send_header('Content-type', 'application/pkcs7')
                  self.end_headers()
                  f = open(os.getcwd() + "/simple.p7b", 'rb')
                  self.wfile.write(f.read())
               else:
                  self.send_response(500, self.path + ' invalid')
                  logging.warning("500: Invalid path " + self.path + "\n")

           logging.warning(" ======================= POST Done =======================")
           logging.warning(" =========================================================")
        else:
           logging.error(" POST is not turned on")

def main(argv):
  global PORT
  global POST

  try:
    opts, args = getopt.getopt(argv, "hp:-post:", ["port=", "post="])
  except getopt.GetoptError:
    print 'Error in arguments\n'
    usage()
    sys.exit(1)
  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ("-p", "--port"):
      PORT = int(arg)
    elif opt in ("--post") and arg.upper() == "ON":
      POST = True

  #Start up server
  if(POST):
    Handler = GetHandlerWithPOST
  else:
    Handler = GetHandler

  server = SocketServer.TCPServer(("", PORT), Handler)
  if(POST):
     print "Serving at port: ", PORT, " POST is ON"
  else:
     print "Serving at port: ", PORT, " POST is OFF"

  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print "\nShutting down Server"
    server.shutdown()



if __name__ == "__main__":
  main(sys.argv[1:])
