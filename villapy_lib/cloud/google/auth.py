"""
Scirpt con el objetivo de realizar la creación y actualización de credenciales
para poder trabajr con la nube
"""

# pyright: reportArgumentType = false
# pyright: reportUnknownMemberType = false
# pyright: reportUnknownVariableType = false
# pyright: reportMissingTypeStubs = false

# pylint: disable=no-member

from typing import Any, Dict, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from villapy_lib.looging.write_log import WriteLogs

class GoogleAuth:
    """ Herramientas de Google que son de gran utilidad """

    def __init__(self, ls_scope: List[str], di_routes: Dict[str,str],
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
        self.ls_scope = ls_scope

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
                     ls_scope: List[str] | None = None)->None:
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
        ls_scope = ls_scope or self.ls_scope

        flow = InstalledAppFlow.from_client_secrets_file(st_route_client, ls_scope)
        creds = flow.run_local_server(port=0)

        with open(st_route_token, 'w', encoding="utf-8") as file:
            file.write(creds.to_json())

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
        ls_scope = ls_scope or self.ls_scope

        creds = Credentials.from_authorized_user_file(st_route_token, ls_scope)
        service = build("drive", "v3", credentials=creds)
        about = service.about().get(fields="user").execute()

        st_text = "Cuenta del token:", about.get("user", {}).get("emailAddress")
        self._logs(st_text)

# Finite Incantatem
