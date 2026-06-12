""" Limpieza de datos

El script contiene todo lo correspondiente a las cadenas de texto
"""

import re

import string
import secrets
import unicodedata
from typing import Dict

import bcrypt

class TextManage:
    """ TextManage """

    def __init__(self) -> None:
        """ TextManage """
        return

    def string_check(self, st_word:str)->str:
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

    def caracters_clean_v2(self, st_file_name:str) -> str:
        """ clean_caracters
        
        Limpia el nombre de carcteres etraños que puedan romper el nombre de la tabla,
        sin numeros

        Parameters:
            st_file_name (str): Nombre con caracteres raros
        Returns:
            st_file_name (str): Nombre sin caracteres raros
        """
        st_file_name = re.sub(pattern='[<>:"/\\|?*´%!@$&()=¿-;_]', repl="",
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

        if ls_pattern:
            st_number = re.findall(r"-?\d+\.\d+", st_number)[0]

        return st_number

    def modify_date(self, st_date:str)->str|None:
        """ Modificación de fecha

        Se da formato a las fechas mal formadas 

        Parameters:
            st_data (str): Fecha con formato incierto

        Returns:
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

    def valid_name(self, st_name:str)->bool:
        """ Validación de Nombres 

        Solo se aceptan letras y acentos, devuelve un booleano

        Parameters:
            st_name (str): Palabra que será evaluada
        Returns:
            bool (bool): True si el nombre es válido, False en caso contrario
        """
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$", st_name))

    def valid_email(self, st_email:str)->bool:
        """ Validación de Correos

       Corrobora que el correo sea correcto en formato y configuración

        Parameters:
            st_email (str): Correo que será evaluado
        Returns:
            bool (bool): True si el correo es válido, False en caso contrario
        """
        if st_email.startswith(".") or st_email.endswith("."):
            return False

        if ".." in st_email:
            return False

        return bool(re.match( r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', st_email))

    def valid_phone(self, st_phone:str)->bool:
        """ Validación de Teléfono

       Corrobora que el teléfono sea correcto en estuctura y secuencia

        Parameters:
            st_phone (str): teléfono que será evaluado
        Returns:
            bool (bool): True si el teléfono es válido, False en caso contrario
        """
        return bool(re.match( r'^[2-9]\d{9}$', st_phone)) and len(st_phone) == 10

    def change_word(self, st_word:str, di_changes: Dict[str, str])->str:
        """ Cambio de Palabras

        Toma el diccionario que proporciona el usuario y cambia las palabras dentro del texto

        Parameters:
            st_word (str): Texto que será modificado
            di_changes (dict): Diccionario con las palabras que serán cambiadas y las nuevas 
        Returns:
           st_word (str): Devuelve el texto con las palabras adecuadas
        """
        for key, item in di_changes.items():
            st_word = st_word.replace(key, item)
        return st_word

    def hash_password(self, st_password:str)->str:
        """ Codificación de la contraseña

        Se codifica la contraseña por seguridad

        Parameters:
            st_password (str): Contraseña que será codificada
        Return:
            hash (str): contraseña codificada 
        """
        st_hashed =bcrypt.hashpw(st_password.encode(), bcrypt.gensalt())
        return st_hashed.decode()

    def create_passwords(self,in_how_pass: int = 1, in_how_long: int = 32)->str:
        """ Creador de contraseñas

        Crea la cantidad de contraseñas requeridas del tamño requerido, intercala letras, digitos
        y simbolos 

        Parameters:
            in_how_pass (int): Cuantas contraseñas requieres, no acepta valores menores a 0 ó 0
            in_how_long (int): Tamaño de la contraseña no acepta valores menores a 0 ó 0

        Return:
            st_save (str): Contraseña o contraseñas 
        """

        in_how_pass = 1 if in_how_pass <= 0 else in_how_pass
        in_how_long = 32 if in_how_long <= 0 else in_how_long

        st_options = string.ascii_letters+string.digits+"!#$-_+=.,"
        st_save = ""

        for _ in range(0, in_how_pass, 1):
            st_password = "".join(secrets.choice(st_options) for _ in range(0, in_how_long, 1))
            st_save = st_save + st_password + "\n"

        return st_save

    def format_bool(self, st_bool: str)-> bool | str: # Falta prueba unitaria 
        """ Formato de booleanos

        Da el formato adecuado al texto que se pretende tomar como booleano
        para ello se debe verificar que el texto contenga true o false

        Parameters:
            st_bool (str): Texto que contiene un booleano
        Returns:
            bo_bool (bool): Booleano correcto
        """

        bo_bool = (True if st_bool.capitalize() == "True" else False 
                   if st_bool.capitalize() == "False" else "NOT")

        return bo_bool

# Finite Incantatem
