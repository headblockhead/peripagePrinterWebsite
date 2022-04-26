#!/usr/bin/env python3

"""
Simple test procedure for manual printing functions of ppa6ctl module
"""
import datetime
import ppa6ctl as printer
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
def take_snap():
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

    cam = cv2.VideoCapture(0)
    ret, image = cam.read()
    cv2.imwrite('./cam.png', image)
    printer.printStart()
    printer.printLn("Time: " + str(datetime.datetime.now()))
    printer.printImage("cam.png")
    printer.printStop()
    cam.release()
    print("Stop printing...")

    print("Disconnecting")
    printer.disconnect()

    error = printer.getLastError()
    if error:
      print("An error occured during test procedure:", error)

    print("End module ppa6ctl test procedure")
