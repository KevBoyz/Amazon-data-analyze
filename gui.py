import PySimpleGUI as sg


def minimize_main_window(main_window):
    main_window.hide()
    layout = [[sg.T('This is your window with a customized titlebar... you just cannot see it')]]
    window = sg.Window(main_window.Title, layout, finalize=True, alpha_channel=0)
    window.minimize()
    window.bind('<FocusIn>', '-RESTORE-')
    minimize_main_window.dummy_window = window


def restore_main_window(main_window):
    if hasattr(minimize_main_window, 'dummy_window'):
        minimize_main_window.dummy_window.close()
        minimize_main_window.dummy_window = None
    main_window.un_hide()

def title_bar(title, text_color, background_color):
    bc = background_color
    tc = text_color
    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, key='-MINIMIZE-'),
                     sg.Text('❎', text_color=tc, background_color=bc, enable_events=True, key='Exit')]], element_justification='r', key='-TITLEBAR-',
                   pad=(0, 0), background_color=bc)]