#!usr/bin/python3.6
import serial
import sys
import os
import time
import re
import PySimpleGUI as sg

sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read() 

global MAX_LOOP_NUM
global newCmd
MAX_LOOP_NUM = 10
 
def waitForCmdOKRsp():
    maxloopNum = 0
    while True:
        line = ser.readline()
        maxloopNum = maxloopNum + 1
        
        try:
            print("Response : %s"%line.decode('utf-8'))
        except:
            pass
            
        if ( re.search(b'OK',line)):
            break
        elif(maxloopNum > MAX_LOOP_NUM):
            sys.exit(0)
 
def sendAT_Cmd(serInstance,atCmdStr,waitforOk):
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))
    #or define b'string',bytes should be used not str
    if(waitforOk == 1):
        waitForCmdOKRsp()
    else:
        waitForCmdRsp()
 
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  
sendAT_Cmd(ser,'AT+CFUN=1\r',1)
sendAT_Cmd(ser,'AT+COPS?\r',1)
ser.close()
