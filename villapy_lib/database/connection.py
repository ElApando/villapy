""" Creación y disponibilización de la Conexión con la base de datos

Para ejecutar => python -m src.connection.connection_db
"""

# pylint: disable=import-error
# pylint: disable=no-name-in-module

from typing import Dict, Any, TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.orm import Session

class Connection:
    """ Connection Data Base """

    def __init__(self, di_conections: Dict[str, str | None], bo_test: bool = False) -> None:
        """ Conexión a la base de datos

        La clase realiza la comunicación del programa a la base dedatos mediante sqlalchemy 
        establece la conexión y la session con la cual se comunica los datos
        """
        self.st_user_db = di_conections["username"]
        self.st_pass_db = di_conections["password"]
        self.st_serv_db = di_conections["server"]
        self.st_data_db = di_conections["database"]
        self.st_driv_db = di_conections["drive"]
        self.bo_test = bo_test

    def get_connection(self) -> "Engine":
        """ Creación de la conexión con la base de datos

        Esta conexión es importante dado que se establece el puente entre la API y el servidor 
        por el cual pasara la información que se pediran a traves de las peticiones, cabe mencionar
        que el driver se bifurca debido a que es diferente para la plataforma que se utilice

        Returns:
            connection (engie): Conexión a la base de datos
        """
        params: Dict[str, Any] = {
                'username' : self.st_user_db,
                'password' : self.st_pass_db,
                'server' : self.st_serv_db,
                'database' : self.st_data_db,
                'driver': self.st_driv_db} 

        connection_string = ('{driver}://{username}:{password}@{server}:3306/{database}'
                                .format(**params))

        if not connection_string:
            raise ValueError("La variable de entorno CONNECTION_STRING no está configurada.")

        connection = (create_engine("sqlite:///:memory:") if self.bo_test else
                      create_engine(connection_string))

        return connection

    def connect_session(self) -> tuple["Session", "Engine"]:
        """Disponibiliza la conexión con la base de datos

        Hace accesible la conexión a las funciones mediante una sesión de sessionmaker
        
        Returns:
            tuple (tuple): Una tupla con dos elementos.
            - db_session (session): Sesión requerida para poder operar los datos dentro de la base
                de datos.
            - db_engine (engine): Conexión a la base de datos en su estado primitivo.
        """
        db_engine = self.get_connection()
        sesion = sessionmaker(bind = db_engine)
        db_session = sesion()

        return db_session, db_engine

# Finite Incantatem
