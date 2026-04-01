""" DOC """

import re
import unicodedata

class TextManage:
    """ TextManage """

    def __init__(self) -> None:
        """ TextManage """
        return

    def string_check(self, st_word:str)->str: # Será eliminada
        """ String_Check

        Revisión de que la palabra sea una cadena de texto

        Parameteres:
            st_word (str): Palabra de evaluación

        Returns:
            st_word (str): Palabra evaluada
        """
        if not self.caracters_clean(st_word):
            raise ValueError(f"La {st_word} es invalida")

        return st_word

    def accent_clean(self, st_text:str) -> str:
        """ clean_accent
        
        Limpieza de los acentos de las palabras

        Parameters:
            st_text (str): Nombre con acentos
        Returns:
            st_text (str): Nombre sin acentos
        """
        return ''.join(
            c for c in unicodedata.normalize('NFKD', st_text)
            if not unicodedata.combining(c)
        )

    def caracters_clean(self, st_file_name:str) -> str:
        """ clean_caracters
        
        Limpia el nombre de carcteres etraños que puedan romper el nombre de la tabla

        Parameters:
            st_file_name (str): Nombre con caracteres raros
        Returns:
            st_file_name (str): Nombre sin caracteres raros
        """
        st_file_name = re.sub(pattern='[<>:"/\\|?*´%!@$&()=¿123456789]', repl="",
                               string = st_file_name)
        return st_file_name

    def save_numbers(self, st_number:str)->str:
        """ Salvación de números

        Se recatan los numeros de los precios que estan mal formados, no aceptan fechas

        Parameters:
            st_number (str): Cadena de texto a evaluar
        
        Returns:
            st_number (str): Número encontrado
        """
        st_number = str(st_number)
        ls_pattern = re.findall(pattern = r"-?\d+\.\d+", string = st_number)
        print(ls_pattern)

        if ls_pattern:
            st_number = re.findall(r"-?\d+\.\d+", st_number)[0]

        return st_number

    def modify_date(self, st_date:str)->str|None:
        """ Modificación de fecha

        Se da formato a las fechas mal formadas 

        Parameters:
            st_data (str): Fecha con formato incierto

        Return:
            st_data (str): Fecha con el formato adecuado 
        """
        di_months = {"jan":"01", "ene":"01", "feb": "02", "mar": "03", "apr": "04", "abr":"04",
                    "may": "05", "jun": "06", "jul":"07", "aug": "08", "ago": "08" , "sep": "09",
                    "oct": "10", "nov": "11", "dic":"12", "dec":"12"}

        ls_one = st_date.split("/")

        if len(ls_one) == 1:
            ls_one = st_date.split("-")

        if len(ls_one) == 1:
            ls_one = st_date.split(".")

        if ls_one[0] in ["", None, "None"]:
            return None

        if ls_one[1].isalpha():
            ls_one[1] = di_months[(ls_one[1]).lower()]
            st_save = ls_one[0]
            ls_one[0] = ls_one[2]
            ls_one[2] = st_save

            if len(ls_one[0]) == 2:
                ls_one[0] = f"20{ls_one[0]}"

        if len(ls_one[2]) == 4:
            st_save = ls_one[0]
            ls_one[0] = ls_one[2]
            ls_one[2] = st_save

        if int(ls_one[1]) > 12:
            st_save = ls_one[2]
            ls_one[2] = ls_one[1]
            ls_one[1] = st_save

        st_date = "-".join(ls_one)

        return st_date

# Finite Incantatem
