import AppGui
import serial
import sys
import re

global MAX_LOOP_NUM
global newCmd
MAX_LOOP_NUM = 10

def waitForCmdOKRsp(serInstance):
    maxloopNum = 0
    while True:
        line = serInstance.readline()
        maxloopNum = maxloopNum + 1
        try:
            print("Answer: %s"%line.decode('utf-8'))
        except:
            pass
        if (re.search(b'OK',line)):
            break
        elif(maxloopNum > MAX_LOOP_NUM):
            sys.exit(0)
 
def sendAT_Cmd(serInstance,atCmdStr,waitforOk):
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))
    #or define b'string',bytes should be used not str
    if(waitforOk == 1):
        waitForCmdOKRsp(serInstance)
    else:
        waitForCmdRsp()


if __name__ == "__main__":
    window = AppGui.sg.Window("Serial Communication", AppGui.window_layout)
    while True:
        event, values = window.read()
        if event == "Start Serial Communication":
            ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  
            sendAT_Cmd(ser,'AT+CFUN=1\r',1)
            sendAT_Cmd(ser,'AT+COPS?\r',1)
            ser.close()
        elif event == "OK" or event == AppGui.sg.WIN_CLOSED:
            break

    window.close()
