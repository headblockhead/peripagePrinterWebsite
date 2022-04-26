#!/usr/bin/env python3

"""
Simple test procedure for manual printing functions of ppa6ctl module
"""
import datetime
import ppa6ctl as printer
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
def print_text(Toprint):
    #mac = printer.search()
    mac = "35:53:19:07:1D:BC"

    if not mac:
      print("No printer found, stopping test procedure")
      exit()

    print("Connecting to: %s" % mac)
    if not printer.connect(mac):
      print("Connection to printer failed, stopping test procedure")
      print("Error:", printer.getLastError())

    print("Is printer connected? %s" % "Yes" if printer.connected() else "No")

    printer.printStart()
    printer.printLn(Toprint)
    printer.printStop()
    print("Stop printing...")

    print("Disconnecting")
    printer.disconnect()

    error = printer.getLastError()
    if error:
      print("An error occured during test procedure:", error)

    print("End module ppa6ctl test procedure")
