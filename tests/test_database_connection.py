""" Prueba Unitaria Conexión a la Base de Datos se cree correctamente
python -m tests.test_database_connection
"""

# pylint: disable = import-outside-toplevel

class TestDataBaseConnection:
    """Prueba Unitaria Creación de Conexión"""

    def test_connection_session(self):
        """ Prueba Unitaria Creación de Conexión
        """

        from villapy_lib.database.connection import Connection
        from sqlalchemy.engine import Engine
        from sqlalchemy.orm import Session

        active = Connection({"username": "user", "password": "pass", "server": "server",
                             "database": "database", "drive": "drive"}, True)
        session = active.connect_session()

        assert isinstance(session[0], Session)
        assert isinstance(session[1], Engine)

# activo = TestDataBaseConnection()
# print(activo.test_connection_session())

# Finite Incantatem
