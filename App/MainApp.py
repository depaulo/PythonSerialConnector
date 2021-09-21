from PySimpleGUI.PySimpleGUI import OK
import AppGui
import serial
import sys
import re

global MAX_LOOP_NUM
global newCmd
MAX_LOOP_NUM = 10

def AD_INIT(serInstance) :
    AD_CMD = [('AT\r',1),('ATI\r',1)]
    cmd_Res = 0
    for atCmdStr,waitForOk in AD_CMD :
        cmd_Res += sendAT_Cmd(serInstance,atCmdStr,waitForOk)
    if cmd_Res == len(AD_CMD) :
        return 1
    else :
        return 0 

def AD_PDPCFG(serInstance) :
    AD_CMD = [('AT\r',1),('ATI\r',1)]
    cmd_Res = 0
    for atCmdStr,waitForOk in AD_CMD :
        cmd_Res += sendAT_Cmd(serInstance,atCmdStr,waitForOk)
    if cmd_Res == len(AD_CMD) :
        return 1
    else :
        return 0 

def AD_INFO(serInstance) :
    AD_CMD = [('AT\r',1),('ATI\r',1)]
    cmd_Res = 0
    for atCmdStr,waitForOk in AD_CMD :
        cmd_Res += sendAT_Cmd(serInstance,atCmdStr,waitForOk)
    if cmd_Res == len(AD_CMD) :
        return 1
    else :
        return 0 

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
            return 1
        elif(maxloopNum > MAX_LOOP_NUM):
            sys.exit(0)
 
def sendAT_Cmd(serInstance,atCmdStr,waitForOk):
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))
    #or define b'string',bytes should be used not str
    if(waitForOk == 1):
        ret = waitForCmdOKRsp(serInstance)
        return int(ret)


if __name__ == "__main__":
    serial_window = AppGui.sg.Window("Serial Seletion", AppGui.serial_selection_layout)
    cmdSpeed = 0
    cmdName = ''
    while True:
        event, values = serial_window.read()
        if event == "OK":
            cmdName = str(values['cmd_name'])
            cmdSpeed = int(values['cmd_speed'])
            break
        elif event == AppGui.sg.WIN_CLOSED:
            serial_window.close()
            sys.exit(0)
            break
    serial_window.close()

    main_window = AppGui.sg.Window("Serial Communication", AppGui.main_window_layout)
    print("Starting serial communication....")
    serInstance = serial.Serial(cmdName, cmdSpeed, timeout=1)
    while True:
        event, values = main_window.read()
        AD_INIT(serInstance)
        if event == "Open PDP context":
            print("Open PDP context")
            AD_PDPCFG(serInstance)
        if event == "INFO":
            print("INFO")
            AD_INFO(serInstance)
        elif event == "OK" or event == AppGui.sg.WIN_CLOSED:
            break
    main_window.close()    
