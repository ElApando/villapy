"""
Docstring for villapy_lib.filesystem.project_creator
python -m villapy_lib.filesystem.project_creator
"""
from pathlib import Path
from typing import Dict, Any, List

from villapy_lib.filesystem.files_utils import ManageFile

class ProjectCreate: # Falta prueba unitaria
    """ Creación de proyectos """

    def __init__(self, di_routes: Dict[str, Any])->None:
        """ Inicio

        La clase tiene el objetivo de crear las carpetas y archivos necesarios para iniciar
        un nuevo proyecto. Para ello se requiere un diccionario en el que se describa el orden
        del mismo. A continuación se mustra un ejemplo:

        DI_ROUTES_ORIGIN: Dict[str, Any] = {
                "Project": {   -> Nombre del proyecto 
                    "config": ["dynamic.py", "static.py"], -> Carpeta con dos archivos
                    "legacy":[], -> Carpeta sin archivos
                    "file": ["main.py", "requirements.txt"]} -> Archivos raíz 

        Nota : Para realizar una carpeta debes de colocar un diccionario.

        Parameters:
            di_routes (Dict): Diccionario con el orden del proyecto"""

        self.cl_manager_file = ManageFile()
        self.st_project = list(di_routes.keys())[0]
        self.di_routes: Dict[str, Any] = di_routes
        self.ls_routes: List[str] = self.check_dict_route(di_data=self.di_routes, in_depth=1)

    def excute(self):
        """ Orquestador

        1- Creación de rutas
        """
        for ii in self.ls_routes:
            st_project_name = ii.replace(f"{self.st_project}/", "")
            self.create_route(st_project_name)

    def check_dict_route(self, di_data: Dict[str, Any], st_save: str = "", 
                         ls_save: List[str] | None  = None, in_depth: int = 1)->List[str]:
        """ Revisión rutas en el diccionario

        Acomoda la estructura del diccionario conla finalidad de acomadar las rutas en una lista
        y sea facil de manejar

        Parameters:
            di_data (Dict): Diccionario con el orden del proyecto
            st_save (str): Ruta inicial o consecutiva del orden
            ls_save (List): Lista que guarda las rutas creadas
            in_depth (int): Profundidad de la carpeta 
        Returns:
            ls_save (List): Lista con todas las rutas provenientes del diccionario
        """
        st_save_route = st_save

        if ls_save is None:
            ls_save = []

        for key, item in di_data.items():
            st_save_route = f"{st_save_route}{key}/"
            ls_save.append(st_save_route)

            if isinstance(item, dict): # Carpeta
                self.check_dict_route(item, st_save_route, ls_save, in_depth+1) # type:ignore

            if isinstance(item, list): # Archivo
                if key != "file":
                    for ii in item: # type:ignore
                        st_save_file = f"{st_save_route}{ii}"
                        ls_save.append(st_save_file)

                else:
                    st_save_route = st_save_route[:st_save_route.find("/")+1]
                    for ii in item: # type:ignore
                        st_save_file = f"{st_save_route}{ii}"
                        ls_save.append(st_save_file)

            ls_previwe = st_save_route.split("/")[0:in_depth-1]
            st_previwe = "/".join(ls_previwe)

            st_save_route = f"{st_previwe}/"

        return ls_save

    def create_route(self, st_route: str)->None:
        """ Creación de rutas 

        Crea la ruta dependiendo si es una carpeta o un archivo, si ya existe la ruta no ocurre
         nada.

        Parameters:
            st_route (str): Ruta en string 
        """

        pa_path = Path(st_route)

        if st_route.find(".") < 0:
            self.cl_manager_file.check_path(pa_path)

        else:
            pa_path.touch()

# Finite Incantatem
