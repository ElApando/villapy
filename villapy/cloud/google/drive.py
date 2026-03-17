"""
DOCT
"""

# pyright: reportUnknownVariableType = false

from typing import Any, Dict, List

from google.oauth2.credentials import Credentials # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from googleapiclient.errors import HttpError # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore

from villapy.looging.write_log import WriteLogs

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
        self.st_folder_id = di_scope["folder_id"]["prd"]
        self.st_route_file = di_routes["file_prd"]
        self.st_name_file = di_routes["name_file"]

        self.bo_type = di_logs["type"]
        self.bo_model = di_logs["mode_file"]
        self.st_word = di_logs["word"]

    def _logs(self, st_text: str)->None:
        """ Registros disponibles  """

        if self.bo_type:
            if self.bo_model:
                self.ac_write.logs_with_name(self.st_word, st_text)
            else:
                self.ac_write.write_logs(st_text)

    def drive_upload_or_replace(self, st_route_file:str = "", st_file_name:str = "",
        st_folder_id:str = "", st_route_token:str = "", ls_scope:List[Any]|None = None)->Any:
        """ Subida o cambio de archivos

        La función sube archivos a Google Drive, primero verifica que no este al ser verdadero lo
        coloca en la ubicación correspondiente, en caso contrario lo rempaza con la nueva versión
        es importante mencionar que para esta función es vital el ID del folder, dado que puede
        causar estragos en el Google Drive.

        Parameters:
            - st_route_file *(str)* - Ruta del archivo en local, es el que se va a subir
            - st_file_name *(str)* - Nombre del archivo que se subira
            - st_folder_id *(str)* - ID del folder en drive piesa clave
            - st_route_token *(str)* - Ruta del archivo token
            - ls_scope *(list)* - Scope que se utiliza para acceder al Drive
        Returns:
            - None -
        """
        st_route_file = st_route_file or self.st_route_file
        st_file_name = st_file_name or self.st_name_file
        st_folder_id = st_folder_id or self.st_folder_id
        st_route_token = st_route_token or self.st_route_token
        ls_scope = ls_scope or self.ls_drive

        creds = Credentials.from_authorized_user_file(st_route_token, ls_scope) # type: ignore
        service = build('drive', 'v3', credentials=creds) # type: ignore

        file_name = st_file_name or st_route_file.split("/")[-1]
        st_text = f"Procesando archivo: {file_name}"
        print(st_text)
        self._logs(st_text)

        # 1) buscar por nombre dentro de la carpeta (soporta Shared Drives)
        q = f"'{st_folder_id}' in parents and name = '{file_name}' and trashed = false"

        try:
            res = service.files().list( q=q, fields="files(id, name)", pageSize=1, # type: ignore
                  supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
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

# Finite incantatem
