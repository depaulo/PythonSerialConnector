import AppGui
import serial
import sys
import re
import traceback

#Function for unpacking the Command List =================================================

def AD_CMDLIST(Message,serInstance,AD_CMD) : #Show informations about the system
    print(Message)
    for atCmdStr in AD_CMD :
        sendAT_Cmd(serInstance,atCmdStr)

#Function for sending the AT Command ========================================================================

def sendAT_Cmd(serInstance,atCmdStr): #The option without the wait for Ok seems good enough.
    print("Command: %s"%atCmdStr)
    serInstance.write(atCmdStr.encode('utf-8'))  #or define b'string',bytes should be used not str
    line = bytearray()
    while serInstance.readline() :
        line.extend(serInstance.readline())
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
            if event == "ComStartPing" :
                AD_CMD = [('ATE0\r'),('AT\r'),('ATI\r'),('AT+CMEE=2\r'),('AT+CREG=2\r')]
                AD_CMDLIST("Starting Serial Communication",serInstance,AD_CMD)
            elif event == "NetCfgPing" :
                AD_CMD = [('AT+COPS=2\r'),('AT+CGDCONT=1,"IP","cat-m1.claro.com.br","0.0.0.0",0,0\r'),('AT^SXRAT=12,7,0\r'),('AT+COPS=0\r'),('AT+COPS?\r')]#('AT+COPS=1,2,72405,7\r')
                AD_CMDLIST("Configuring the internet",serInstance,AD_CMD)
            elif event == "InfoShowPing" :
                AD_CMD = [('AT+CGDCONT?\r'),('AT^SXRAT?\r'),('AT^SMONI\r'),('AT+CREG?\r'),('AT+COPS?\r')]
                AD_CMDLIST("Showing Modem Info",serInstance,AD_CMD)
            elif event == "MainProcPing":
                AD_CMD = [('AT+CGATT=1\r'),('AT^SICA=1,1\r'),('AT+CGPADDR=1\r'),('AT^SISX=PING,1,"8.8.8.8",5,5000\r')]
                AD_CMDLIST("Main Procedure...",serInstance,AD_CMD)
            elif event == "ButtonPing":
                AD_CMD = [(str(values['TextInputPing'])+'\r')]
                AD_CMDLIST("Custom Command",serInstance,AD_CMD)
            elif event == "ComStartTrans" :
                AD_CMD = [('ATE0\r'),('AT\r'),('ATI\r'),('AT+CMEE=2\r'),('AT+CREG=2\r')]
                AD_CMDLIST("Starting Serial Communication",serInstance,AD_CMD)
            elif event == "NetCfgTrans":
                AD_CMD = [('AT+COPS=2\r'),('AT+CGDCONT=1,"IP","cat-m1.claro.com.br","0.0.0.0",0,0\r'),('AT^SISS=0,srvtype,socket\r'),('AT^SISS=0,conid,1\r'),('AT^SISS=0,alphabet,1\r'),('at^siss=0,address,"sockudp://123.456.789.000:12345"\r'),('AT+COPS=0\r'),('AT+COPS?\r')]#('AT+COPS=1,2,72405,7\r')
                AD_CMDLIST("Configuring the internet",serInstance,AD_CMD)
            elif event == "InfoShowTrans" :
                AD_CMD = [('AT+CGDCONT?\r'),('AT^SXRAT?\r'),('AT^SMONI\r'),('AT+CREG?\r'),('AT+COPS?\r')]
                AD_CMDLIST("Showing Modem Info",serInstance,AD_CMD)
            elif event == "MainProcTrans":
                AD_CMD = [('AT+CGPADDR=1\r'),('AT^SICA=1,1\r'),('AT^SISO=0\r')]
                AD_CMDLIST("Main Procedure...",serInstance,AD_CMD)
            elif event == "ButtonTrans":
                AD_CMD = [(str(values['TextInputTrans'])+'\r')]
                AD_CMDLIST("Custom Command",serInstance,AD_CMD)
            elif event == "OK" or event == AppGui.sg.WIN_CLOSED:
                break
        main_window.close()
    except Exception as e:
        main_window.close()    
        tb = traceback.format_exc()
        AppGui.sg.popup_error_with_traceback(f'COMUNICATION PROBLENS', e, tb)