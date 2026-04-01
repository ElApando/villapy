"""
El script tiene como objetivo gestionar todo lo que tiene que ver con google drive
desde permisos para escritura, modificación y creación de archivos.
"""

# pyright: reportUnknownVariableType = false

# pylint: disable = undefined-variable
# pylint: disable = no-member

from typing import Any, Dict, List

from google.oauth2.credentials import Credentials # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from googleapiclient.errors import HttpError # type: ignore

from villapy_lib.looging.write_log import WriteLogs

class GoogleTools:
    """ Herramientas de Google que son de gran utilidad """

    def __init__(self, di_scope: Dict[str, Any], di_routes: Dict[str,str],
                 di_logs: Dict[str, Any])->None:
        """ Herramientas google

        La clase contiene diferentes funciones que permiten la interacción con google, esta clase
        se enfoca en:
            - El manejo de archivos:
                - Puede subir archivos o remplazarlos.
                - Crea tokens de seguridad.
                - Revisar si estos están activos.
        """
        self.ac_write = WriteLogs()

        self.st_route_token = di_routes["token"]
        self.ls_drive = di_scope["scope"]["drive"]

        self.di_scope = di_scope
        self.di_routes = di_routes

        self.bo_type = di_logs["type"]
        self.bo_model = di_logs["mode_file"]
        self.st_word = di_logs["word"]

        self.service = self.config_drive(self.st_route_token, self.ls_drive)

    def _logs(self, st_text: str)->None:
        """ Registros disponibles  """

        if self.bo_type:
            if self.bo_model:
                self.ac_write.logs_with_name(self.st_word, st_text)
            else:
                self.ac_write.write_logs(st_text)

    def config_drive(self, st_token: str, ls_scope: List[Any]|None = None)->Any: # Falta Prueba Unitaria
        """ Configuración de credenciales 

        La función toma le token y configura las credenciales necesarias para poder acceder
        a los archivos y carpetas en drive

        Parameters:
            st_toke (str): Ruta en la que se encuentra el token con los permisos
            ls_scope (List): Contine el scope al que se quiere acceder
        
        Returns:
            service (Class): Permisos configurados, listos para ser utilizados
        """
        creds = Credentials.from_authorized_user_file(st_token, ls_scope) # type: ignore
        service = build('drive', 'v3', credentials=creds) # type: ignore
        return service

    def drive_upload_or_replace(self, st_route_file:str = "", st_file_name:str = "",
        st_folder_id:str = "")->Any:
        """ Subida o cambio de archivos

        La función sube archivos a Google Drive, primero verifica que no este al ser verdadero lo
        coloca en la ubicación correspondiente, en caso contrario lo rempaza con la nueva versión
        es importante mencionar que para esta función es vital el ID del folder, dado que puede
        causar estragos en el Google Drive.

        Parameters:
            - st_route_file *(str)* - Ruta del archivo en local, es el que se va a subir
            - st_file_name *(str)* - Nombre del archivo que se subira
            - st_folder_id *(str)* - ID del folder en drive piesa clave
        Returns:
            - None -
        """
        st_route_file = st_route_file or self.di_routes["file_prd"]
        st_file_name = st_file_name or self.di_routes["name_file"]
        st_folder_id = st_folder_id or self.di_scope["folder_id"]["prd"]

        file_name = st_file_name or st_route_file.split("/")[-1]
        st_text = f"Procesando archivo: {file_name}"
        print(st_text)
        self._logs(st_text)

        # 1) buscar por nombre dentro de la carpeta (soporta Shared Drives)
        q = f"'{st_folder_id}' in parents and name = '{file_name}' and trashed = false"

        try:
            res = self.service.files().list( q=q, fields="files(id, name)", # type: ignore
            pageSize=1, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        except HttpError as e:
            raise RuntimeError(f"Error al listar archivos en la carpeta: {e}") from e

        files = res.get('files', []) # type: ignore
        media = MediaFileUpload(st_route_file, resumable=True)

        if files:
            # -> existe: actualizar (replace)
            file_id = files[0]['id'] # type: ignore
            try:
                st_text = f"Archivo existente encontrado. Reemplazando id={file_id} ..."
                print(st_text)
                self._logs(st_text)
                updated = service.files().update( fileId=file_id, media_body=media, # type: ignore
                          supportsAllDrives=True).execute()
                st_text = f"Reemplazado: {file_name} (id: {updated.get('id')})" # type: ignore
                print(st_text)
                self._logs(st_text)
                return updated # type: ignore
            except HttpError as e:
                # permisos insuficientes u otros errores
                raise RuntimeError(f"Error actualizando el archivo (update): {e}") from e
        else:
            # -> no existe: crear dentro de la carpeta
            file_metadata:Dict[str,str] = {"name": file_name,"parents": [st_folder_id]}#type:ignore

            try:
                st_text = "Archivo no existe. Creando nuevo archivo en la carpeta..."
                print(st_text)
                self._logs(st_text)
                created = service.files().create(body=file_metadata, media_body=media, #type:ignore
                                            fields="id, name", supportsAllDrives=True).execute()
                st_text = f"Creado: {created.get('name')} (id: {created.get('id')})" #type:ignore
                print(st_text)
                self._logs(st_text)
                return created # type: ignore

            except HttpError as e:
                raise RuntimeError(f"Error creando el archivo (create): {e}") from e

    def query_drive_mapper(self, st_folder_id: str)->List[str]: # Falta prueba unitaria
        """ Extracción de contenido

        La función extrae el contenido del folder en cuestión para ello se usa el id del folder

        Parameters:
            st_folder_id (str): id del folder de interes

        Returns:
            files (List): Lista con los documentos o folder que encontro  
         """

        result = self.service.files().list( q = f"'{st_folder_id}' in parents", # type: ignore
                                    fields = "files(id, name, mimeType)",
                                    supportsAllDrives = True,
                                    includeItemsFromAllDrives = True).execute()
        files = result.get("files", []) # type: ignore

        return files

    def mapper_drive(self, files:List[Any], di_container: Dict[str,Any],
                     ls_except: List[str])->Dict[str,Any]: # Falta prueba unitaria
        """ Mapeador de carpetas
         
        La función mapea todas las carpetas dentro de esta y debajo, generando un diccionario con
        las mismas
         
        Parameters:
            files (List): Lista de id's perteneciente a los archivos presentes
            di_container (Dict): Diccionario vacio en el que se almacena el contenido de la carpeta
            ls_except (List): Lista con las excepciones de busqueda
        Returns:
            di_container (Dict): Diccionario con todo el mapeo
        """

        for file in files :
            if "document" in file["mimeType"] or any( prefix in file["name"]
                                                     for prefix in ls_except):
                continue

            di_container[file["name"]] = {
                "id": file["id"]
            }

            if "folder" in file["mimeType"]:
                sub_files = self.query_drive_mapper(file["id"])
                di_container[file["name"]]["file"] = {}
                self.mapper_drive(sub_files, di_container[file["name"]]["file"], ls_except)

        return di_container

# Finite incantatem
