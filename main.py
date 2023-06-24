from geopy.geocoders import Nominatim
import requests
import pandas as pd
from popups import *
from route import *
from windows import *
from utils import *
import webbrowser
import os
import sys


def read_load_file(file_path=None, window=None):
    '''
    Leitura do arquivo xlsx inserido
    '''
    df = pd.DataFrame()
    if file_path:
        df = pd.read_excel(file_path)
    if df.empty or file_path is None:
        return None
    
    required_columns = ['CIDADE', 'BAIRRO', 'LONGITUDE', 'LATITUDE', 'ORIGEM']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        no_columns(missing_columns)
        df, file_path, missing_columns = set_none(df, file_path, missing_columns)
        return

    if window is not None:
        update_gui(window, df)
    return df


def start_address(origin_address, df, window):
    """
    Nominatim - encontra as coordenadas da origem
    Organiza display
    """
    geolocator = Nominatim(user_agent="EndiroTSPProject")
    coordenadas_origem = []
    
    while True:
        location_origin = geolocator.geocode(query=origin_address, addressdetails=True)
        if location_origin:
            coordenadas_origem.append((location_origin.latitude, location_origin.longitude))
            update_gui(window, df, location_origin=location_origin)
            break
        else:
            origin_address = start_address_second_input(df, resource_path)
            if origin_address is None:
                return  # Retorna para reiniciar o programa
            
    return coordenadas_origem


def resource_path(relative_path):
    """ 
    Pega o caminho absoluto de arquivos externos
    """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    window = main_window(icon, resource_path)
    validate = False
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == '-READ-':
            file_path = values['-FILE-']
            df = read_load_file(window=window, file_path=file_path)
            if not isinstance(df, pd.DataFrame):
                no_file_popup()
            else:
                df_show_origin = df['ORIGEM'].iloc[0]
                origin_address = df.loc[0, 'ORIGEM']
                coordenadas_origem = start_address(origin_address, df_show_origin, window)
                validate = True
        
        if event == '-EDIT-':
            popup_message("Funcionalidade em desenvolvimento!")

        if (event == '-START_1-' or event == '-CTRL_1-') and not values['-QUANTITY-'] == '' and not values['-CITY-'] == '':

            qt_addresses = values['-QUANTITY-']
            selected_city = values['-CITY-']
            df_filtered = df.loc[(df['CIDADE'] == selected_city)]
            coordinates = [(float(row["LATITUDE"]), float(row["LONGITUDE"])) for _, row in df_filtered.head(int(qt_addresses)).iterrows()]
            clients_display = [f"{row['CLIENTE']}, {row['ENDERECO']}, {row['BAIRRO']}" for _, row in df_filtered.head(int(qt_addresses)).iterrows()]
            if coordenadas_origem is None:
                continue
            
            coord_list_1 = first_try(coordenadas_origem[0], coordinates)

            # Criando link da primeira tentativa #
            url = "https://www.google.com/maps/dir/"
            for i in range(len(coord_list_1)-1):
                url += f'{coord_list_1[i][0]}, {coord_list_1[i][1]}/'
            url += f'{coord_list_1[-1][0]}, {coord_list_1[-1][1]}'
            
            response = requests.get(url)
            if response.status_code == 200:
                webbrowser.open(response.url) 
            else:
                popup_message(response.status_code)
        
        # SEGUNDA ESTRATÉGIA #
        if (event == '-START_2-' or event == '-CTRL_2-') and not values['-QUANTITY-'] == '' and not values['-CITY-'] == '':
            qt_addresses = values['-QUANTITY-']
            selected_city = values['-CITY-']
            df_filtered = df.loc[(df['CIDADE'] == selected_city)]
            origin_address = df.loc[0, 'ORIGEM']
            coordinates = [(float(row["LATITUDE"]), float(row["LONGITUDE"])) for _, row in df_filtered.head(int(qt_addresses)).iterrows()]
            df_show_origin = df['ORIGEM'].iloc[0]
            
            if coordenadas_origem is None:
                continue
            
            coord_list_1_2 = first_try(coordenadas_origem[0], coordinates)
            aux_list = [x for x in coord_list_1_2[1:]]
            coord_list_2 = second_try(aux_list)
            new_list = []
            for i in coord_list_2:
                new_list.append(aux_list[i])

            new_list.insert(0, coordenadas_origem[0])

            # Criando link da segunda tentativa #
            url = "https://www.google.com/maps/dir/"
            for i in range(len(new_list)-1):
                url += f'{new_list[i][0]}, {new_list[i][1]}/'
            url += f'{new_list[-1][0]}, {new_list[-1][1]}'

            response = requests.get(url)
            if response.status_code == 200:
                webbrowser.open(response.url) 
            else:
                popup_message(response.status_code)

        # TERCEIRA ESTRATÉGIA # - até 11 endereços para uma busca otimizada
        if (event == '-START_3-' or event == '-CTRL_3-') and not values['-QUANTITY-'] == '' and not values['-CITY-'] == '':
            qt_addresses = values['-QUANTITY-']
            if qt_addresses <= 11:
                validate = True
            else:
                # Validação acima de 11 endereços #
                validate = too_much_addresses_confirm_popup(qt_addresses)
            
            if validate == True:
                selected_city = values['-CITY-']
                df_filtered = df.loc[(df['CIDADE'] == selected_city)]
                origin_address = df.loc[0, 'ORIGEM']
                coordinates = [(float(row["LATITUDE"]), float(row["LONGITUDE"])) for _, row in df_filtered.head(int(qt_addresses)).iterrows()]
                df_show_origin = df['ORIGEM'].iloc[0]

                if coordenadas_origem is None:
                    continue
                
                coord_list_4 = tsp_branch_and_bound(coordenadas_origem + coordinates)

                url_4 = "https://www.google.com/maps/dir/"
                for i in range(len(coord_list_4)-1):
                    url_4 += f'{coord_list_4[i][0]}, {coord_list_4[i][1]}/'
                url_4 += f'{coord_list_4[-1][0]}, {coord_list_4[-1][1]}'
                
                response = requests.get(url_4)
                if response.status_code == 200:
                    webbrowser.open(response.url) 
                else:
                    popup_message(response.status_code)
            else:
                continue
        else:
            pass

    window.close()

if __name__ == '__main__':
    icon = resource_path('icon.ico')
    main()
