class GoogleTools:
    """ Herramientas de Google que son de gran utilidad """

    def __init__(self)->None:
        """ Herramientas google

        La clase contiene diferentes funciones que permiten la interacción con google, esta clase
        se enfoca en:
            - El manejo de archivos:
                - Puede subir archivos o remplazarlos.
                - Crea tokens de seguridad.
                - Revisar si estos están activos.

        Parameters:
            - None -
        Returns:
            - None -
        """
        self.st_route_client = static.DI_ROUTES["client"]
        self.st_route_token = static.DI_ROUTES["token"]
        self.ls_drive = static.DI_SCOPE_TABLES["scope"]["drive"]
        self.ls_metadata = static.DI_SCOPE_TABLES["scope"]["metadata"]
        self.st_folder_id = static.DI_SCOPE_TABLES["folder_id"]["prd"]
        self.st_route_file = static.DI_ROUTES["file_prd"]
        self.st_name_file = static.DI_ROUTES["name_file"]

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
        write_logs("general", st_text)

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

        st_text = "Cuenta del token:", about.get("user", {}).get("emailAddress") # type: ignore
        write_logs("general", st_text) # type: ignore

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
        write_logs("general", st_text)

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
                write_logs("general", st_text)
                updated = service.files().update( fileId=file_id, media_body=media, # type: ignore
                          supportsAllDrives=True).execute()
                st_text = f"Reemplazado: {file_name} (id: {updated.get('id')})" # type: ignore
                print(st_text)
                write_logs("general", st_text)
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
                write_logs("general", st_text)
                created = service.files().create(body=file_metadata, media_body=media, #type:ignore
                                            fields="id, name", supportsAllDrives=True).execute()
                st_text = f"Creado: {created.get('name')} (id: {created.get('id')})" #type:ignore
                print(st_text)
                write_logs("general", st_text)
                return created # type: ignore

            except HttpError as e:
                raise RuntimeError(f"Error creando el archivo (create): {e}") from e