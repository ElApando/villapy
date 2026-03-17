""" DOC """

import os
import json
import shutil
from pathlib import Path
from typing import Dict

from villapy.looging.write_log import WriteLogs

class OpenFiles:
    """ OpenFiles """

    def __init__(self) -> None:
        """ OpenFiles 
        
        La clase agrupa la apertura, scritura y modificación de diferentes tipos de archivos,
        Se sigue trabajando en ella.
        """

    def open_json(self, st_route_dict:str) -> Dict[str, str]:
        """ open_json

        Abre archivos json y los convierte en un diccionario

        Parameters:
            st_route_dict (str): Ruta en la que s localiza el json

        Returns:
            di_json (dict): Json convertido en diccionario
        """
        with open(st_route_dict, "r", encoding="utf-8") as file:
            di_json = json.load(file)

        return di_json


class ManageFile:
    """ ManageFile """

    def __init__(self) -> None:
        """ ManageFile 
        
        La clase agrupa la apertura, scritura y modificación de diferentes tipos de archivos,
        Se sigue trabajando en ella.
        """
        self.logs_activate = WriteLogs()

    def move_file(self, pa_path_origing:Path, pa_path_final:Path, st_type:str)->None:
        """ Movimiento de archivos

        Copia o Corta el archivo del destino de origen y lo pega en la carpeta correspondiente

        Parameters:
            pa_path_origing (Path): Ruta de origen del archivo
            pa_path_final (Path): Ruta en la que se colocara el archivo de interes
            st_type (str): Tipo de movimiento que se realizará, ya sea [CUT, COPY]  
        """
        st_type = st_type.upper()
        pa_path_origing = Path(pa_path_origing)
        pa_path_final = Path(pa_path_final)

        if st_type == "CUT":
            pa_path_origing.rename(pa_path_final)

        elif st_type == "COPY":
            shutil.copy2(pa_path_origing, pa_path_final)

        else:
            raise KeyError("Esa Opción no existe en el método")

    def check_path(self, pa_path:Path)->None:
        """ Revisión de rutas

        Revisa que la ruta ingresada sea valida en los diferentes sistemas operativos, además de
         crear la ruta si no existe

        Parameters:
            pa_path (Path): Ruta que será revisada
        """

        if not self._validate_path(pa_path):
            raise ValueError("Ruta Invalida")

        if not os.path.exists(pa_path):
            os.makedirs(pa_path, exist_ok=True)


    def _validate_path(self, pa_path:Path)->bool:
        """  _validate_path

        Revisión de que el Path es valido
        
        Parameters:
            pa_path (Path): Ruta qeu será evaluada 
        
        Return:
            bool: Retorna un booleano indicando si es valida la ruta o no
        """
        try:
            Path(pa_path).resolve()
            return True

        except Exception as e:
            self.logs_activate.write_logs(f"{e}")
            return False

    def separator_table(self, pa_path:Path)->str:
        """ separator_table

        Se obtiene el separador de los archivos CSV y TXT, dado que en ocasiones los archivos
        se encuentran sucios.

        Parameters:
            pa_path (Path): Ruta del archivo

        Returns:
            st_separator (str): Separador de datos, necesario para hacer la extracción de datos
            con pandas
        """
        st_path = Path(pa_path)

        with st_path.open("r", encoding = "utf-8") as file:
            content = file.readline()

        st_separator = self._separator_what(content)

        return st_separator

    def _separator_what(self, st_word:str)->str:
        """ separator_what

        Los archivos en ocaciónes se encuentran suciós por lo que se busca es que tipo de separador
        tiene el archivo.

        Parameters:
            st_word (str): Cadena de texto que se revisa
        """
        if "|" in st_word:
            st_separator = "|"

        elif ";" in st_word:
            st_separator = ";"

        elif "\t" in st_word:
            st_separator = "\t"

        elif "," in st_word:
            st_separator = ","

        else:
            raise ValueError("Separador no encontrado")

        return st_separator

# Finite Incantatem
