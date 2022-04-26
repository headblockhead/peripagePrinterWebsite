import cv2
import datetime
import ppa6ctl as printer
import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '0.0.0.0'    # Change this to your Raspberry Pi IP address
host_port = 8000
mac = "35:53:19:07:1D:BC"

class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command 
            'curl http://server-ip-address:port' 
        """
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Welcome to my raspberry pi!</h1>
            <p>Take snap? <a href="/snap">Snap</a></p>
            <p>Print Text? <a href="/print/testText">Print</a></p>
            <div id="led-status"></div>
            <script>
                document.getElementById("led-status").innerHTML="{}";
            </script>
            </body>
            </html>
        '''
        self.do_HEAD()
        if self.path=='/':
             print("home")
        elif self.path=='/snap':
             ret, image = cam.read()
             cv2.imwrite('./cam.png', image)
             printer.printLn("Time: " + str(datetime.datetime.now()))
             printer.printImage("cam.png")
        elif 'print' in self.path:
            printer.printLn(self.path[7:])
        self.wfile.write(html.format('', '').encode("utf-8"))
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    cam = cv2.VideoCapture(0)
    printer.connect(mac)
    printer.printStart()
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        printer.printStop()
        cam.release()
        printer.disconnect()
