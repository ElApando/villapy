"""
DOCT
"""

from typing import Any, Dict, List

from google.oauth2.credentials import Credentials # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from googleapiclient.errors import HttpError # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore

from villapy.looging.write_log import WriteLogs


class GoogleAuth:
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
        self.st_route_client = di_routes["client"]
        self.st_route_token = di_routes["token"]
        self.ls_drive = di_scope["scope"]["drive"]

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

    def drive_create_token(self, st_route_client:str = "", st_route_token:str = "",
                     ls_scope: str = "")->None:
        """ Crecaión del Token Google

        La función crea un token de seguridad, con google, no se requiere ingresar repetidas veces
        las credenciales, se ingresa solo una vez y con eso funciona sin problemas.

        Parameters:
            - st_route_client *(str)* - Ruta del archivo con los acceso del cliente archivo .json
            - st_route_token *(str)* - Ruta donde estara el token
            - ls_scope *(list)* - Scope que se utiliz para crear el token
        Returns:
            - None -
        """
        st_route_client =st_route_client or self.st_route_client
        st_route_token = st_route_token or self.st_route_token
        ls_scope = ls_scope or self.ls_drive

        flow = InstalledAppFlow.from_client_secrets_file(st_route_client, ls_scope) # type: ignore
        creds = flow.run_local_server(port=0) # type: ignore

        with open(st_route_token, 'w', encoding="utf-8") as file:
            file.write(creds.to_json()) # type: ignore

        st_text = f"token.json creado con éxito, en la siguiente ruta {st_route_token}"
        print(st_text)
        self._logs(st_text)

    def drive_check_token(self, st_route_token:str = "", ls_scope: List[Any]|None = None)->None:
        """ Revisión del Token Google

        La función revisa que el token que se maneja en el flujo u otro cualquiera funcione
        correctamente, debe de aparecer el correo con el que se trabaja, si no es así se debe
        de revisar que token se utiliza

        Parameters:
            - st_route_token *(str)* - Ruta donde estara el token
            - ls_scope *(list)* - Scope que se utiliza para crear el token
        Returns:
            - None -
        """
        st_route_token = st_route_token or self.st_route_token
        ls_scope = ls_scope or self.ls_drive

        print(st_route_token,ls_scope)

        creds = Credentials.from_authorized_user_file(st_route_token, ls_scope) # type: ignore
        service = build("drive", "v3", credentials=creds) # type: ignore
        about = service.about().get(fields="user").execute() # type: ignore

        st_text = str("Cuenta del token:", about.get("user", {}).get("emailAddress")) # type:ignore
        self._logs(st_text)
