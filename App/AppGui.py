import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

inputs_layout = [
    [sg.Text("Hello from PySimpleGUI")],
    [sg.Button("Start Serial Communication")],
    [sg.Button("OK")]
]

output_layout = [
    [sg.Text("Anything printed will display here!")],
    [sg.Output(size=(60,15), font='Courier 8')]
]

main_window_layout = [
    [sg.Column(inputs_layout, element_justification='c'),
    sg.Column(output_layout, element_justification='c')]
]

serial_selection_layout = [
    [sg.Text('Choose Boarding place',size=(20, 1), font='Lucida',justification='left')],
    [sg.Combo(['New York','Chicago','Washington', 'Colorado','Ohio','San Jose','Fresno','San Fransisco'],default_value='Unselected')],
    [sg.Button("OK")]
]


if __name__ == "__main__":
    main_window = sg.Window("Serial Communication", main_window_layout)
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
