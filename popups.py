import PySimpleGUI as sg


def success_popup():
    popup_layout = [
        [sg.Text('Carregado!')],
        [sg.Button('OK', key='-LOADED-')]
    ]
    popup_window = sg.Window('Pronto', popup_layout, modal=True, finalize=True)
    popup_window.bind("<Escape>", "-ESCAPE-")
    popup_window.bind("<Return>", "-RETURN-")
    while True:
        popup_event, popup_values = popup_window.read()
        if popup_event in (sg.WINDOW_CLOSED, '-LOADED-', "-ESCAPE-", "-RETURN-"):
            break
    popup_window.close()


def no_file_popup():
    layout_popup = [
        [sg.Text('Selecione um arquivo .xlsx primeiro!')],
        [sg.Button('OK', key='-NOTLOADED-')]
    ]
    popup_window = sg.Window('Ops!', layout_popup, modal=True, finalize=True)
    popup_window.bind("<Escape>", "-ESCAPE-")
    popup_window.bind("<Return>", "-RETURN-")
    while True:
        popup_event, popup_values = popup_window.read()
        if popup_event in (sg.WINDOW_CLOSED, '-NOTLOADED-', "-ESCAPE-", "-RETURN-"):
            break
    popup_window.close()


def no_columns(columns):
    message = f"Faltaram as seguintes colunas: \n {columns}"

    layout = [
        [sg.Text(message)],
        [sg.Button("OK")]
    ]
    
    window = sg.Window("Ops!", layout, modal=True, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "OK":
            break

    window.close()


def popup_message(msg):
    popup_layout = [
        [sg.Text(f"{msg}", key='-MSG-')],
    ]
    
    popup_window = sg.Window('Ops! Erro na criação da página', popup_layout, finalize=True, modal=True)
    popup_window.bind("<Escape>", "-ESCAPE-")
    popup_window.bind("<Return>", "-RETURN-")
    while True:
        popup_event, popup_values = popup_window.read()
        if popup_event in (sg.WINDOW_CLOSED, '-URLERROR-', '-ESCAPE-', "-RETURN-"):
            break
    popup_window.close()


def too_much_addresses_confirm_popup(qt_addresses):
    button_color = ('#faf8f8', '#16537e')
    
    layout_popup = [
        [sg.Push(), sg.Text(f'Você selecionou {qt_addresses} endereços'), sg.Push()],
        [sg.Text('Acima de 11 endereços, esse cálculo tende a demorar')],
        [sg.Text('')],
        [sg.Push(), sg.Text('Deseja continuar?', justification='center'), sg.Push()],
        [sg.Push(), sg.Button('SIM', key='-YES-', button_color=button_color, size=10), sg.Push(),
        sg.Button('NÃO', key='-NO-', button_color=button_color, size=10), sg.Push()]
        ]
    sg.theme('DefaultNoMoreNagging')
    popup_window = sg.Window('Aviso!', layout_popup, modal=True, finalize=True)
    popup_window.bind("<Escape>", "-ESCAPE-")
    popup_window.bind("<Return>", "-RETURN-")
    while True:
        popup_event, popup_values = popup_window.read()
        if popup_event in (sg.WINDOW_CLOSED, '-NO-', "-ESCAPE-"):
            break
        if popup_event in ('-YES-', "-RETURN-"):
            popup_window.close()
            return True
    popup_window.close()

if __name__ == '__main__':
    pass
