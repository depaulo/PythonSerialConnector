import os
import PySimpleGUI as sg

#MAIN WINDOW LAYOUT


inputs_Tab_Ping = [
    [sg.Text("PythonSerialConnector -- PING --",pad=(0,20))],
    [sg.Button("Start Communication",key='ComStartPing',size=(20,1))],
    [sg.Button("Internet Configuration",key='NetCfgPing',size=(20,1))],
    [sg.Button("Show INFO",key='InfoShowPing',size=(20,1))],
    [sg.Button("Main Procedure",key='MainProcPing',size=(20,1))],
    [sg.Text('Custom Commands', size =(20, 1))], 
    [sg.InputText(key='TextInputPing',size =(40, 1))],
    [sg.Button("Input",key='ButtonPing',bind_return_key=True)]
]

inputs_Tab_Transp = [
    [sg.Text("PythonSerialConnector -- TRANSPARENT TCP SOCKET --",pad=(0,20))],
    [sg.Button("Start Communication",key='ComStartTrans',size=(20,1))],
    [sg.Button("Internet Configuration",key='NetCfgTrans',size=(20,1))],
    [sg.Button("Show INFO",key='InfoShowTrans',size=(20,1))],
    [sg.Button("Main Procedure",key='MainProcTrans',size=(20,1))],
    [sg.Text('Custom Commands', size =(20, 1))], 
    [sg.InputText(key='TextInputTrans',size =(40, 1))],
    [sg.Button("Input",key='ButtonTrans',bind_return_key=True)]
]

output_layout = [
    [sg.Text("Anything printed will display here!")],
    [sg.Output(size=(70,20), font='Courier 10')]
]

main_window_layout = [
    [sg.Column([[sg.TabGroup([[sg.Tab('PING',inputs_Tab_Ping),sg.Tab('TRANSP SERIAL',inputs_Tab_Transp)]])]]),sg.Column(output_layout, element_justification='c')],
    [sg.Button("OK",pad=(0,20))]
]

#SERIAL WINDOW LAYOUT

if os.name == 'nt' :
    serial_selection_layout = [
        [sg.Text('Choose Device Serial Configuration',size=(30, 1), font='Lucida',justification='left')],
        [sg.Combo(['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18','COM19','COM20'],size=(10,1), key='cmd_name', default_value='COM5')],
        [sg.Combo(['9600','115200'],size=(10,1), key='cmd_speed', default_value='115200')],
        [sg.Button("OK")]
    ]
else :
    serial_selection_layout = [
        [sg.Text('Choose Device Serial Configuration',size=(20, 1), font='Lucida',justification='left')],
        [sg.Combo(['/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3'],size=(10,1), key='cmd_name',default_value='Unselected')],
        [sg.Combo(['9600','115200'],size=(10,1), key='cmd_speed', default_value='115200')],
        [sg.Button("OK")]
    ]    

#MAIN PROGRAM, UTILIZADO PARA VERIRIFICAÇÃO DE MODIFICAÇÕES

if __name__ == "__main__":
    main_window = sg.Window("PythonSerialConnector - Serial Communication -- GTI32 V0.9 -- ", main_window_layout)
    serial_window = sg.Window("Serial Seletion", serial_selection_layout)
    while True:
        s_event, s_values = serial_window.read()
        if s_event == "OK":
            serial_window.close()
            while True:
                m_event, m_values = main_window.read()
                if m_event == "Start Serial Communication":
                    print("Starting serial communication....")
                elif m_event == "OK" or m_event == sg.WIN_CLOSED:
                    break
            break
        elif s_event == sg.WIN_CLOSED:
            serial_window.close()
            break
    main_window.close()
