import PySimpleGUI as sg


def main_window(icon, resource_path):
    '''
    Janela principal
    '''
    value_qt_addresses = [i for i in range(1, 25)]
    sg.set_global_icon(icon)
    sg.theme('DefaultNoMoreNagging')
    font_selectors = ('Arial', 10, 'bold')
    button_font = ('Arial', 10)
    font_example = ('Arial', 6)
    button_color = ('#faf8f8', '#16537e')
    button_off_color = ('#bcbcbc', '#5b5b5b')
    main_button_size = (20, 2)
    button_size = (15, 2)
    display_pad = ((15, 10), (0, 10))
    multiline_standard_size = (43, 2)
    horizontal_line_pad = (0, 10)
    icon_size = (35, 35)

    layout = [
        [sg.Text('Modelo da planilha: ', font=font_example)],
        [sg.Text('PAIS | CLIENTE | CIDADE | UF | ENDERECO | BAIRRO | LATITUDE | LONGITUDE | ORIGEM', font=font_example)],
        [sg.HorizontalSeparator(pad=horizontal_line_pad)],
        [sg.FileBrowse('Selecionar arquivo (.xlsx)', size=main_button_size, button_color=button_color, 
                        file_types=(("Excel Files", "*.xlsx"),), key='-FILE-', enable_events=True), sg.Push(), 
        sg.Button('Carregar', key='-READ-', size=main_button_size, button_color=button_color)],
        [sg.HorizontalSeparator(pad=horizontal_line_pad)],
        [sg.Multiline(justification='c', default_text='Endereço de origem irá aparecer aqui', size=multiline_standard_size,
                      key="-ORIGIN_DISPLAY-", disabled=True, autoscroll=False, background_color='', 
                      text_color=button_color[1], visible=True, no_scrollbar=True), 
                      sg.Button('', image_filename=resource_path('edit.png'), key='-EDIT-', image_size=icon_size)],
        [sg.Text('Quantidade', font=font_selectors), sg.Push(), sg.Text('Cidade', font=font_selectors), sg.Push()],
        [sg.Push(), sg.Combo(value_qt_addresses, key='-QUANTITY-', button_background_color=button_color[1], readonly=True, size=(20, 10)), sg.Push(), 
        sg.Combo(values=[], button_background_color=button_color[1], key='-CITY-', readonly=True, size=(20, 10), enable_events=True), sg.Push()],
        [sg.Button('1ª ROTA', key='-START_1-', size=button_size, button_color=button_off_color, font=button_font),
        sg.Button('2ª ROTA', key='-START_2-', size=button_size, button_color=button_off_color, font=button_font),
        sg.Button('3ª ROTA', key='-START_3-', size=button_size, button_color=button_off_color, font=button_font), sg.Push()],
        
    ]
    # Create Window #
    
    window = sg.Window("Melhor rota 1.0", layout, grab_anywhere=False, size=(480, 360),
                        element_padding=(5,5), scaling=1.6, default_button_element_size=(5, 2), finalize=True)
    
    window.bind("<Shift_L><!>", "-CTRL_1-")
    window.bind("<Shift_L><@>", "-CTRL_2-")
    window.bind("<Shift_L><#>", "-CTRL_3-")

    return window


def start_address_second_input(df_show_origin, resource_path):
    """
    Janela secundária
    Endereço não encontrado
    """
    sg.theme('DefaultNoMoreNagging')
    font = ('Arial', 11)
    font_example = ('Arial', 6)
    layout = [
        [sg.Text('Não foi possível encontrar o endereço inserido na planilha', font=font,)],
        [sg.HorizontalSeparator()],
        [sg.Text('Endereço inserido:', font=font_example)],
        [sg.Text(df_show_origin, font=font, background_color='#f7b9b9', key='-SHOW_ORIGIN-')],
        [sg.HorizontalSeparator()],
        [sg.Text('Por favor, insira novamente o endereço:',)],
        [sg.Text('Ex: Rua dos Andradas, 222 Tatuapé São Paulo SP', font=font_example)],
        [sg.InputText(key='-ORIGIN-', size=(55, ), )],
        [sg.Button('', image_filename=resource_path('lupa.png'), key='-SEARCH-')],
    ]
    window = sg.Window('Endereço de partida', layout, modal=True, finalize=True)
    window.bind("<Return>", "-RETURN-")
    input_element = window['-ORIGIN-']
    input_element.set_focus()

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            window.close()
            return None
        elif event in ('-SEARCH-', "-RETURN-"):
            user_input = values['-ORIGIN-']
            window.close()
            return user_input


def change_start_address(origin_address, resource_path):
    """
    ALTERAÇÃO DE ENDEREÇO DE ORIGEM EM TEMPO DE EXECUÇÃO
    Não utilizada ainda
    """
    sg.theme('DefaultNoMoreNagging')
    font = ('Arial', 11)
    font_example = ('Arial', 6)
    layout = [
        [sg.Text('Endereço atual:', font=font_example)],
        [sg.Text(origin_address, font=font, key='-SHOW_ORIGIN-')],
        [sg.HorizontalSeparator()],
        [sg.Text('Insira novo endereço:',)],
        [sg.Text('Ex: Rua dos Andradas, 222 Tatuapé São Paulo SP', font=font_example)],
        [sg.InputText(key='-ORIGIN-', size=(55, ), )],
        [sg.Button('', image_filename=resource_path('lupa.png'), key='-SEARCH-')],
    ]
    window = sg.Window('Endereço de partida', layout)
    

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            window.close()
            return None
        elif event == '-SEARCH-':
            user_input = values['-ORIGIN-']
            window.close()
            return user_input

