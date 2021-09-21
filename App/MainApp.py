from PySimpleGUI.PySimpleGUI import OK
from time import sleep
import AppGui
import serial
import sys
import re
import traceback


global MAX_LOOP_NUM
global newCmd
MAX_LOOP_NUM = 10


def AD_INIT(serInstance) : #Initial configuration for the system
    AD_CMD = [('ATE0\r'),('AT\r'),('ATI\r'),('AT+CMEE=1')]
    SUM_OK = 0
    for atCmdStr in AD_CMD :
        SUM_OK += sendAT_Cmd(serInstance,atCmdStr)
    print('SUM_OK='+str(SUM_OK)+'\r')


def AD_PDPCFG(serInstance) : #Internet configuration
    AD_CMD = [('AT+COPS=2\r'),('AT+CGDCONT=1,"IP","java.claro.com.br","0.0.0.0",0,0\r'),('AT+COPS=0\r'),('AT+COPS?\r')]
    SUM_OK = 0
    for atCmdStr in AD_CMD :
        SUM_OK += sendAT_Cmd(serInstance,atCmdStr)     
    print('SUM_OK='+str(SUM_OK)+'\r')


def AD_INFO(serInstance) : #Show informations about the system
    AD_CMD = [('AT^SMONI\r'),('AT+CREG?\r'),('AT+COPS?\r')]
    SUM_OK = 0
    for atCmdStr in AD_CMD :
        SUM_OK += sendAT_Cmd(serInstance,atCmdStr)
    print('SUM_OK='+str(SUM_OK)+'\r')


def AD_CUSTOMCMD(serInstance,customCmd) : #Sends a custom Command
    AD_CMD = [(customCmd+'\r',0)]
    for atCmdStr,waitForOk in AD_CMD :
        sendAT_Cmd(serInstance,atCmdStr,waitForOk)


def sendAT_Cmd(serInstance,atCmdStr,waitForOk=1):
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))  #or define b'string',bytes should be used not str
    line = bytearray()
    if waitForOk == 1 :
        while serInstance.readline() :
            line.extend(serInstance.readline())
            sleep(1)
            if (re.search(b'OK',line)):
                print("Answer: %s"%line.decode('utf-8'))
                return 1
        print("Answer: %s"%line.decode('utf-8'))
        return 0
    else :
        while serInstance.readline() :
            line.extend(serInstance.readline())
            sleep(1)
        print("Answer: %s"%line.decode('utf-8'))
        return 0


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
    serial_window.close()
    try:
        serInstance = serial.Serial(cmdName, cmdSpeed, timeout=1)
    except Exception as e:
        tb = traceback.format_exc()
        AppGui.sg.popup_error_with_traceback(f'PROBLEMS WHILE OPPENING SERIAL COMMUNICATION', e, tb)
    main_window = AppGui.sg.Window("Serial Communication", AppGui.main_window_layout)
    try:
        print("Connection OK!!!!")
        while True:
            event, values = main_window.read()
            if event == "Start Communication":
                print("Starting Communication")
                AD_INIT(serInstance) 
            elif event == "Internet Configuration":
                print("Configuring the internet")
                AD_PDPCFG(serInstance) 
            elif event == "Show INFO":
                print("Showing Modem Info")
                AD_INFO(serInstance)
            elif event == "Input":
                print("Custom Command")
                AD_CUSTOMCMD(serInstance,str(values['TextInput']))
            elif event == "OK" or event == AppGui.sg.WIN_CLOSED:
                break
        main_window.close()
    except Exception as e:
        main_window.close()    
        tb = traceback.format_exc()
        AppGui.sg.popup_error_with_traceback(f'COMUNICATION PROBLENS', e, tb)