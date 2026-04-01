""" Prueba Unitaria de importaciones de módulos """

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel

class TestImportModuls:
    """ Clase de Pruebas de Unitarias de Importar Módulos"""

    def test_imports_library(self):
        """ Prueba Unitaria Importación de Módulo - Libreria"""
        import villapy_lib

    def test_imports_dependencies(self):
        """ Prueba Unitaria Importación de Módulo - Dependencias"""
        import villapy_lib.cloud
        import villapy_lib.config
        import villapy_lib.data
        import villapy_lib.database
        import villapy_lib.filesystem
        import villapy_lib.looging
        import villapy_lib.utils

    def test_imports_cloud(self):
        """ Prueba Unitaria Importación de Módulo - Nube"""
        import villapy_lib.cloud.azure
        import villapy_lib.cloud.google

    def test_imports_config(self):
        """ Prueba Unitaria Importación de Módulo - Configuración"""
        import villapy_lib.config.dynamic
        import villapy_lib.config.static

    def test_imports_data(self):
        """ Prueba Unitaria Importación de Módulo - Datos"""
        import villapy_lib.data.dataframe
        import villapy_lib.data.text

    def test_imports_database(self):
        """ Prueba Unitaria Importación de Módulo - Base de Datos"""
        import villapy_lib.database.connection
        import villapy_lib.database.query
        import villapy_lib.database.sqlite

    def test_imports_filesystem(self):
        """ Prueba Unitaria Importación de Módulo - Sistema de Archivos"""
        import villapy_lib.filesystem.files_utils
        import villapy_lib.filesystem.mapper
        import villapy_lib.filesystem.path_utils

# Finite Incantatem
