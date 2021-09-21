from pickle import PicklingError
from PySimpleGUI.PySimpleGUI import OK
from time import sleep
import AppGui
import serial
import sys
import re
import traceback

testSelection = 2

if testSelection == 1 :
    #Serial Communication Scripts - PING =================================================

    def AD_PDPCFG(serInstance) : #Internet configuration
        AD_CMD = [('AT+COPS=2\r'),('AT+CGDCONT=1,"IP","cat-m1.claro.com.br","0.0.0.0",0,0\r'),('AT^SXRAT=12,7,0\r'),('AT+COPS=0\r'),('AT+COPS?\r')]#('AT+COPS=1,2,72405,7\r')
        for atCmdStr in AD_CMD :
            sendAT_Cmd(serInstance,atCmdStr)   

    def AD_MAIN(serInstance) : #Show informations about the system
        AD_CMD = [('AT+CGATT=1\r'),('AT^SICA=1,1\r'),('AT+CGPADDR=1\r'),('AT^SISX=PING,1,"8.8.8.8",5,5000\r')]
        for atCmdStr in AD_CMD :
            sendAT_Cmd(serInstance,atCmdStr)


elif testSelection == 2 :
    #Serial Communication Scripts - TRANSPARENT TCP SOCKET  =================================================

    def AD_PDPCFG(serInstance) : #Internet configuration
        AD_CMD = [('AT+COPS=2\r'),('AT+CGDCONT=1,"IP","cat-m1.claro.com.br","0.0.0.0",0,0\r'),('AT^SISS=0,srvtype,socket\r'),('AT^SISS=0,conid,1\r'),('AT^SISS=0,alphabet,1\r'),('at^siss=0,address,"sockudp://123.456.789.000:12345"\r'),('AT+COPS=0\r'),('AT+COPS?\r')]#('AT+COPS=1,2,72405,7\r')
        for atCmdStr in AD_CMD :
            sendAT_Cmd(serInstance,atCmdStr)     


    def AD_MAIN(serInstance) : #Show informations about the system
        AD_CMD = [('AT+CGPADDR=1\r'),('AT^SICA=1,1\r'),('AT^SISO=0\r')]
        for atCmdStr in AD_CMD :
            sendAT_Cmd(serInstance,atCmdStr)


#Serial Communication Scripts - COMMON =================================================


def AD_INIT(serInstance) : #Initial configuration for the system
    AD_CMD = [('ATE0\r'),('AT\r'),('ATI\r'),('AT+CMEE=2\r'),('AT+CREG=2\r')]
    for atCmdStr in AD_CMD :
        sendAT_Cmd(serInstance,atCmdStr)  


def AD_INFO(serInstance) : #Show informations about the system
    AD_CMD = [('AT+CGDCONT?\r'),('AT^SXRAT?\r'),('AT^SMONI\r'),('AT+CREG?\r'),('AT+COPS?\r')]
    for atCmdStr in AD_CMD :
        sendAT_Cmd(serInstance,atCmdStr)


def AD_CUSTOMCMD(serInstance,customCmd) : #Sends a custom Command
    AD_CMD = [(customCmd+'\r')]
    for atCmdStr in AD_CMD :
        sendAT_Cmd(serInstance,atCmdStr)

#Serial communication ========================================================================

def sendAT_Cmd(serInstance,atCmdStr): #The option without the wait for Ok seems good enough.
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))  #or define b'string',bytes should be used not str
    line = bytearray()
    while serInstance.readline() :
        line.extend(serInstance.readline())
        sleep(0.3)
    print("Answer: %s"%line.decode('utf-8'))
    return 0
    #(re.search(b'OK',line))



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
                print("Starting Serial Communication")
                AD_INIT(serInstance) 
            elif event == "Internet Configuration":
                print("Configuring the internet")
                AD_PDPCFG(serInstance) 
            elif event == "Show INFO":
                print("Showing Modem Info")
                AD_INFO(serInstance)
            elif event == "Main Procedure":
                print("Main Procedure...")
                AD_MAIN(serInstance)
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