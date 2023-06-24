def set_none(*args):
    '''
    Qualquer argumento passado será retornado None
    '''
    result = [None] * len(args)
    return result


def update_gui(window, df, location_origin=None, **kwargs):
    '''
    Todas as atualizações feitas em tempo de execução das janelas
    '''
    # Main window #
    if location_origin is None:
        window['-CITY-'].update(values=df['CIDADE'].unique().tolist())
        window['-READ-'].update(button_color=('#faf8f8', '#16537e'))
        window['-START_1-'].update(button_color=('#ffffff', '#0C7700'))
        window['-START_2-'].update(button_color=('#ffffff', '#0C7700'))
        window['-START_3-'].update(button_color=('#ffffff', '#0C7700'))
    # Endereço de origem #

    if location_origin is not None:
        rua = location_origin.raw['address'].get('road', '')
        numero = location_origin.raw['address'].get('house_number', '')
        cidade = location_origin.raw['address'].get('city', '')
        estado = location_origin.raw['address'].get('state', '')
        bairro = location_origin.raw['address'].get('suburb', '')
        pais = location_origin.raw['address'].get('country', '')
        endereco_formatado = f"{rua}, {numero}, {cidade}, {estado}, {bairro}, {pais}"
        window['-ORIGIN_DISPLAY-'].update(endereco_formatado)