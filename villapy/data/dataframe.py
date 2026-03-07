"""
Docstring for data.dataframe
"""

import pandas as pd

from villapy.data.text import TextManage

class ManageTable:
    """ Manejo de Tablas DataFrame """

    def __init__(self):
        """ Manejo de Tablas DataFrame """
        self.text_active = TextManage()

    def format_column(self, df_data:pd.DataFrame, ls_names:list[str],
                      st_type_data:str)->pd.DataFrame:
        """ Convierte el tipo de dato de columnas específicas de un DataFrame.

        Parameters:
            - df_data *(pd.DataFrame)* - DataFrame original.
            - ls_names *(list)* - Lista de columnas a convertir.
            - st_type_data *(str)* - Tipo de dato destino ("str", "int", "float", "date").

        Retorna:
            - df_data *(pd.DataFrame)* - Nuevo DataFrame con las columnas convertidas.
        """
        for col in ls_names:
            if not col in df_data.columns:
                raise KeyError("La columna ingresada no está contenida en el DataFrame!")

        if st_type_data == "str":
            for col in ls_names:
                df_data[col] = df_data[col].astype(str).replace("nan",None) # type:ignore
                df_data[col] = df_data[col].apply(lambda word: word.strip()) # type:ignore
                df_data[col] = df_data[col].str.upper()
                df_data[col] = df_data[col].apply(self.text_active.caracters_clean) # type:ignore
                df_data[col] = df_data[col].apply(self.text_active.accent_clean) # type:ignore

        elif st_type_data == "int":
            for col in ls_names:
                df_data[col] = (pd.to_numeric(df_data[col], errors='coerce') # type:ignore
                                .fillna(0).astype(int))

        elif st_type_data == "float":
            for col in ls_names:
                df_data[col] = df_data[col].apply(self.text_active.save_numbers) # type:ignore
                df_data[col] = (pd.to_numeric(df_data[col], errors='coerce') # type:ignore
                                .fillna(0).astype(float))

        elif st_type_data == "date":
            for col in ls_names:
                df_data[col] =  df_data[col].apply(self.text_active.modify_date) # type:ignore
                df_data[col] = pd.to_datetime(df_data[col], errors='coerce')

        elif st_type_data == "time":
            for col in ls_names:
                df_data[col] = (pd.to_datetime(df_data[col], format = "%H:%M", errors="coerce")
                                .dt.time)

        else:
            raise KeyError("Esa opcion no existe!")

        return df_data

# Finite Incantatem
